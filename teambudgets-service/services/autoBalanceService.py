import logging
from model.trabajador import Trabajador
from model.equipo import Equipo
from model.proyecto import Proyecto
from services.costesEquipoService import calcular_coste_equipo_por_mes

"""_summary_

curl -X 'GET' \
  'http://localhost:8000/equipo/autobalance/681686f56166caa24736087a/2025-05' \
  -H 'accept: application/json'
  
"""

# Configuración del logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


# Clase para controlar globalmente las horas disponibles por trabajador
class ControlHorasTrabajador:
    def __init__(self, trabajadores: list):
        self.horas_disponibles = {
            t["id"]: t["total-horas"] for t in trabajadores
        }

    def asignar_horas(self, trabajador_id: str, horas: float) -> float:
        disponibles = self.horas_disponibles.get(trabajador_id, 0.0)
        horas_asignadas = min(disponibles, horas)
        self.horas_disponibles[trabajador_id] = max(0.0, disponibles - horas_asignadas)
        return horas_asignadas

    def resumen(self):
        return self.horas_disponibles


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
def procesar_proyecto(proyecto_id: str, proyecto_model, coste_equipo, control_horas):
    
    #---------------------------------------------------------------------
    # 1.- Recuperamos el proyecto y realizmos las validaciones pertinentes
    #---------------------------------------------------------------------
    proyecto = proyecto_model.get_by_id(proyecto_id)
    if not proyecto:
        logging.warning(f"Proyecto con ID {proyecto_id} no encontrado.")
        return None, f"Proyecto con ID {proyecto_id} no encontrado. Revise que el equipo tenga los proyectos asignados correctamente.", 0.0

    logging.info(f"Proyecto '{proyecto.get('nombre')}' encontrado.")

    horas = proyecto.get("horas", {"venta": 0, "consumidas": 0})
    if not horas or "venta" not in horas or "consumidas" not in horas:
        return None, f"Error: Proyecto con ID {proyecto_id} no tiene la información completa de horas." , 0.0

    margen_contrato = proyecto.get("margen-contrato", {})
    if "margen" not in margen_contrato:
        return None, f"Error: Proyecto con ID {proyecto_id} no tiene el margen de contrato informado." , 0.0

    tarifa_hora = proyecto.get("tarifa-hora", 0)
    if tarifa_hora == 0:
        return None, f"Error: Proyecto con ID {proyecto_id} no tiene la tarifa por hora informada." , 0.0

    #---------------------------------------------------------------------
    # 2.- Realizamos las acciones sobre el proyecto
    #---------------------------------------------------------------------
    horas_restantes = (horas["venta"] * (1 - margen_contrato["margen"])) - horas["consumidas"] # Horas que quedan de proyecto
    valor_restante = tarifa_hora * horas_restantes                                             # Valor económico del proyecto

    imputaciones = []
    total_balance = 0

    # Buscamos afinidades a través de los tags de workpool. Harán match los proyectos y trabajadores con un 
    # mismo workpool.
    for trabajador in coste_equipo["trabajadores"]:
        workpools_trabajador = trabajador.get("workpool", [])
        workpools_proyecto = proyecto.get("workpool", [])
        logging.debug(f"Evaluando workpool para Trabajador: {trabajador.get('nombre')} Proyecto: {proyecto.get('nombre')} -> Workpools trabajador {str(workpools_trabajador)}, Workpools proyecto: {str(workpools_proyecto)}")

        
        # Verificamos si hay algún workpool compartido entre trabajador y proyecto
        hay_afinidad = any(wp in workpools_trabajador for wp in workpools_proyecto)
        if hay_afinidad:
            logging.info(f"Se ha encontrado afinidad para {trabajador.get('nombre')} con alguna workpool {str(workpools_trabajador)} y del proyecto {str(workpools_proyecto)}")
            
            # Calculamos las horas que puede imputar este trabajador al proyecto
            horas_a_imputar = control_horas.asignar_horas(trabajador["id"], horas_restantes)

            # Calculamos el coste de imputar esas horas
            coste_hora = trabajador["coste-hora-mensual"]
            coste_horas = round(horas_a_imputar * coste_hora, 2)

            # Añadimos la imputación al listado del proyecto
            imputaciones.append({
                "id": trabajador["id"],
                "nombre": trabajador["nombre"],
                "oficina": trabajador["oficina"],
                "imputacion": {
                    "horas-a-imputar": horas_a_imputar,
                    "coste-horas-a-imputar": coste_horas
                }
            })

            # Sumamos al balance total y reducimos las horas restantes del proyecto
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
def asignar_trabajadores_forzados(proyectos_info, trabajadores, total_balance, control_horas):
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

            horas_a_imputar = control_horas.asignar_horas(trabajador["id"], horas_disponibles)
            if horas_a_imputar == 0:
                continue

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
            break

    return proyectos_info, total_balance

# Función principal que coordina el cálculo del balance de un equipo
def calcular_balance_equipo(equipo_id: str, yyyy_mm: str):
    equipo = obtener_equipo(equipo_id)
    
    retval = {
        "status": "KO",
        "mes": yyyy_mm,
        "equipo-id": equipo.get('_id'),
        "equipo-nombre": equipo.get('nombre'),
        "estructura-costes": {}, 
        "imputaciones": [], 
        "logs": []
    }
    
    #1.- Validaciones previas y obtención de los costes  
    if not equipo:
        retval["logs"].append(f"ERROR: No se encontró el equipo con id {equipo_id}")
        return retval

    coste_equipo = obtener_coste_equipo(equipo_id, yyyy_mm)
    if not coste_equipo:
        retval["logs"].append(f"ERROR: No se pudo calcular el coste del equipo con id {equipo_id}")
        return retval

    retval['estructura-costes'] = coste_equipo
    proyecto_model = Proyecto()
    proyectos_info = []
    logs = []
    total_balance = 0

    #2.- Obtenemos los proyectos asignados al equipo. Estos representan los ingresos.
    control_horas = ControlHorasTrabajador(coste_equipo["trabajadores"])
    for proyecto_id in equipo.get("proyectos", []):
        proyecto_info, error, balance = procesar_proyecto(proyecto_id, proyecto_model, coste_equipo, control_horas)
        if error:
            retval['logs'].append(error)
            return retval
        
        proyectos_info.append(proyecto_info)
        total_balance += balance

    proyectos_info, total_balance = asignar_trabajadores_forzados(
        proyectos_info, coste_equipo["trabajadores"], total_balance,control_horas
    )

    logging.info("Cálculo finalizado para todos los proyectos.")
    
    retval['status'] = "OK"
    retval['imputaciones'] = proyectos_info
    retval['horas-sin-imputar'] = control_horas.resumen()
    retval['logs'] = logs
    return retval