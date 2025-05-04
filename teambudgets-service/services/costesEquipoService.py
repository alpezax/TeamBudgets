from model.trabajador import Trabajador
from model.equipo import Equipo
from model.oficina import Oficina
from datetime import datetime
from utils.objectid_to_str import objectid_to_str
from dateutil.relativedelta import relativedelta
from typing import List

def calcular_coste_equipo_por_mes(equipo_id: str, yyyy_mm: str):
    equipo_model = Equipo()
    trabajador_model = Trabajador()
    oficina_model = Oficina()

    equipo = equipo_model.get_by_id(equipo_id)
    if not equipo:
        return {"error": "Equipo no encontrado"}

    if "miembros" not in equipo or not equipo["miembros"]:
        return {"error": "El equipo no tiene miembros definidos"}

    trabajadores_info = []
    total_horas = 0
    total_coste = 0.0

    for miembro in equipo["miembros"]:
        trabajador_id = str(miembro.get("trabajador_id"))
        participacion = miembro.get("participacion", 100)
        if not trabajador_id:
            return {"error": "ID de trabajador no definido en el equipo"}

        trabajador = trabajador_model.get_by_id(trabajador_id)
        if not trabajador:
            return {"error": f"Trabajador con ID {trabajador_id} no encontrado"}

        nombre = trabajador.get("nombre")
        oficina_id = trabajador.get("oficina")
        if not nombre or not oficina_id:
            return {"error": f"Información incompleta para el trabajador {trabajador_id}"}

        oficina = oficina_model.get_by_id(oficina_id)
        if not oficina:
            return {"error": f"No se encontró la oficina con ID {oficina_id} para el trabajador {nombre}"}
        nombre_oficina = oficina.get("simbolo", "desconocido")

        coste_hora = trabajador_model.get_coste_hora_mensual(trabajador_id, yyyy_mm)
        if coste_hora is None:
            return {"error": f"Coste hora no definido para el trabajador {nombre} ({trabajador_id}) en {yyyy_mm}"}

        dedicacion = trabajador_model.get_dedicacion_mensual(trabajador_id, yyyy_mm) or {}
        dias_vacaciones = dedicacion.get("vacaciones", 0)

        dias_laborables = oficina_model.get_dias_laborables(oficina_id,yyyy_mm)
        if dias_laborables is None:
            return {"error": f"No se pudo calcular los días laborables para la oficina '{nombre_oficina}' ({oficina_id}) y fecha {yyyy_mm}"}

        dias_imputables = dias_laborables - dias_vacaciones
        horas_completas = dias_imputables * 8
        horas_ponderadas = horas_completas * (participacion / 100)
        coste_trabajador = round(horas_ponderadas * coste_hora, 2)

        trabajadores_info.append({
            "id": trabajador_id,
            "nombre": nombre,
            "oficina": {"id": oficina_id, "nombre": nombre_oficina},
            "participacion": participacion,
            "dias-laborables_mes": dias_laborables,
            "dias-vacaciones": dias_vacaciones,
            "dias-imputables": dias_imputables,
            "total-horas": round(horas_ponderadas, 2),
            "coste-hora-mensual": coste_hora,
            "coste-trabajador": coste_trabajador,
            "desc": f"{nombre} ({nombre_oficina}) tiene una participación del {participacion}%. "
                    f"Días imputables: {dias_imputables}, que representan {horas_completas} horas completas. "
                    f"Aplicando el {participacion}%: {round(horas_ponderadas, 2)} horas. "
                    f"Coste: {coste_hora} €/h x {round(horas_ponderadas, 2)} h = {coste_trabajador} €"
        })

        total_horas += horas_ponderadas
        total_coste += coste_trabajador

    return objectid_to_str({
        "fecha": yyyy_mm,
        "nombre-equipo": equipo.get("nombre"),
        "id": equipo_id,
        "trabajadores": trabajadores_info,
        "totales": {
            "total-horas": round(total_horas, 2),
            "coste": round(total_coste, 2)
        }
    })

def forecast_coste_equipo(equipo_id: str, yyyy_mm_inicio: str, n_meses: int) -> List[dict]:
    try:
        fecha_inicio = datetime.strptime(yyyy_mm_inicio, "%Y-%m")
    except ValueError:
        return {"error": "Formato de fecha inválido. Usa 'YYYY-MM'"}

    resultados_forecast = []

    for i in range(n_meses):
        fecha_obj = fecha_inicio + relativedelta(months=i)
        yyyy_mm = fecha_obj.strftime("%Y-%m")
        resultado = calcular_coste_equipo_por_mes(equipo_id, yyyy_mm)

        # Si hay un error, se incluye también en la lista para visibilidad
        resultados_forecast.append({
            "mes": yyyy_mm,
            "resultado": resultado
        })

    return resultados_forecast