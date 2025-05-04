import logging
from model.trabajador import Trabajador
from model.equipo import Equipo
from model.proyecto import Proyecto
from services.costesEquipoService import calcular_coste_equipo_por_mes

# Configuración del logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

# Recupera y valida un equipo por su ID
def obtener_equipo(equipo_id: str):
    equipo_model = Equipo()
    equipo = equipo_model.get_by_id(equipo_id)
    if not equipo:
        logging.error(f"Equipo con ID {equipo_id} no encontrado.")
        return None
    logging.info(f"Equipo '{equipo.get('nombre')}' encontrado.")
    return equipo

# Calcula el coste del equipo para un mes dado
def obtener_coste_equipo(equipo_id: str, yyyy_mm: str):
    coste_equipo = calcular_coste_equipo_por_mes(equipo_id, yyyy_mm)
    if "error" in coste_equipo:
        logging.error(f"No se pudo calcular el coste del equipo para {yyyy_mm}.")
        return None
    logging.info(f"Coste total del equipo calculado correctamente.")
    return coste_equipo

# Procesa la información y balance de un único proyecto
def procesar_proyecto(proyecto_id: str, proyecto_model, coste_equipo):
    proyecto = proyecto_model.get_by_id(proyecto_id)
    if not proyecto:
        logging.warning(f"Proyecto con ID {proyecto_id} no encontrado.")
        return None, f"Proyecto con ID {proyecto_id} no encontrado."

    logging.info(f"Proyecto '{proyecto.get('nombre')}' encontrado.")

    horas = proyecto.get("horas", {"venta": 0, "consumidas": 0})
    if not horas or "venta" not in horas or "consumidas" not in horas:
        return None, f"Error: Proyecto con ID {proyecto_id} no tiene la información completa de horas."

    margen_contrato = proyecto.get("margen-contrato", {})
    if "margen" not in margen_contrato:
        return None, f"Error: Proyecto con ID {proyecto_id} no tiene el margen de contrato informado."

    tarifa_hora = proyecto.get("tarifa-hora", 0)
    if tarifa_hora == 0:
        return None, f"Error: Proyecto con ID {proyecto_id} no tiene la tarifa por hora informada."

    horas_restantes = (horas["venta"] * (1 - margen_contrato["margen"])) - horas["consumidas"]
    valor_restante = tarifa_hora * horas_restantes

    imputaciones = []
    total_balance = 0

    for trabajador in coste_equipo["trabajadores"]:
        if any(wp in trabajador.get("workpool", []) for wp in proyecto.get("workpool", [])):
            horas_a_imputar = min(horas_restantes, trabajador["total-horas"])
            coste_horas = round(horas_a_imputar * trabajador["coste-hora-mensual"], 2)

            imputaciones.append({
                "id": trabajador["id"],
                "nombre": trabajador["nombre"],
                "oficina": trabajador["oficina"],
                "imputacion": {
                    "horas-a-imputar": horas_a_imputar,
                    "coste-horas-a-imputar": coste_horas
                }
            })

            total_balance += coste_horas
            horas_restantes -= horas_a_imputar

    proyecto_info = {
        "_id": proyecto_id,
        "nombre": proyecto.get("nombre"),
        "idext": proyecto.get("idext"),
        "descripcion": proyecto.get("descripcion"),
        "horas": horas,
        "margen-contrato": margen_contrato,
        "workpool": proyecto.get("workpool", []),
        "tarifa-hora": tarifa_hora,
        "imputaciones": imputaciones
    }

    return proyecto_info, None, total_balance

# Asigna trabajadores no asignados a proyectos de forma forzada
def asignar_trabajadores_forzados(proyectos_info, trabajadores, total_balance):
    trabajadores_asignados = {
        t["id"] for p in proyectos_info for t in p["imputaciones"]
    }
    trabajadores_no_asignados = [
        t for t in trabajadores if t["id"] not in trabajadores_asignados
    ]

    for trabajador in trabajadores_no_asignados:
        for proyecto in proyectos_info:
            horas_ya_imputadas = sum(
                imp["imputacion"]["horas-a-imputar"] for imp in proyecto["imputaciones"]
            )
            horas_objetivo = (proyecto["horas"]["venta"] * (1 - proyecto["margen-contrato"]["margen"])) - proyecto["horas"]["consumidas"]
            horas_disponibles = horas_objetivo - horas_ya_imputadas

            if horas_disponibles <= 0:
                continue

            horas_a_imputar = min(horas_disponibles, trabajador["total-horas"])
            coste = round(horas_a_imputar * trabajador["coste-hora-mensual"], 2)

            proyecto["imputaciones"].append({
                "id": trabajador["id"],
                "nombre": trabajador["nombre"],
                "oficina": trabajador["oficina"],
                "imputacion": {
                    "horas-a-imputar": horas_a_imputar,
                    "coste-horas-a-imputar": coste,
                    "asignacion-forzada": True
                }
            })

            total_balance += coste
            break  # Solo lo asignamos a un proyecto

    return proyectos_info, total_balance

# Función principal que coordina el cálculo del balance de un equipo
def calcular_balance_equipo(equipo_id: str, yyyy_mm: str):
    equipo = obtener_equipo(equipo_id)
    if not equipo:
        return {"total_coste": 0.0, "detalles": [], "logs": []}

    coste_equipo = obtener_coste_equipo(equipo_id, yyyy_mm)
    if not coste_equipo:
        return {
            "total_coste": 0.0,
            "estructura-de-costes": coste_equipo,
            "detalles": [],
            "logs": []
        }

    proyecto_model = Proyecto()
    proyectos_info = []
    logs = []
    total_balance = 0

    for proyecto_id in equipo.get("proyectos", []):
        proyecto_info, error, balance = procesar_proyecto(proyecto_id, proyecto_model, coste_equipo)
        if error:
            logs.append(error)
            continue
        proyectos_info.append(proyecto_info)
        total_balance += balance

    proyectos_info, total_balance = asignar_trabajadores_forzados(
        proyectos_info, coste_equipo["trabajadores"], total_balance
    )

    logging.info("Cálculo finalizado para todos los proyectos.")

    return {
        "total_coste": round(coste_equipo["totales"]["coste"], 2),
        "detalles": proyectos_info,
        "logs": logs
    }
