from model.proyecto import Proyecto
from model.equipo import Equipo

# Instanciamos los modelos
proyecto_model = Proyecto()
equipo_model = Equipo()


def calcular_avance(proyecto: dict) -> dict:
    horas_venta = proyecto.get("horas", {}).get("venta", 0)
    horas_consumidas = proyecto.get("horas", {}).get("consumidas", 0)
    margen = proyecto.get("margen-contrato", {}).get("margen", 0)
    tarifa = proyecto.get("tarifa-hora", 0)

    horas_disponibles = (1 - margen) * horas_venta or 1  # evitar división por cero

    porcentaje_consumido = horas_consumidas / horas_disponibles
    porcentaje_restante = 1 - porcentaje_consumido
    dinero_venta = horas_venta * tarifa

    avance = {
        "horas-venta": horas_venta,
        "horas-consumidas": horas_consumidas,
        "porcentaje-consumido": porcentaje_consumido,
        "porcentaje-restante": porcentaje_restante,
        "dinero-venta": dinero_venta
    }

    return {**proyecto, "avance": avance}


def get_all_proyectos():
    """Devuelve todos los proyectos existentes en la base de datos, enriquecidos con avance."""
    proyectos = proyecto_model.get_all()
    return [calcular_avance(p) for p in proyectos]


def get_proyectos_de_equipo(equipo_id: str):
    """
    Dado un ID de equipo, devuelve la lista de proyectos asociados a ese equipo,
    enriquecidos con avance.
    """
    proyectos_ids = equipo_model.get_proyectos_by_id(equipo_id)
    if not proyectos_ids:
        return []

    proyectos = []
    for pid in proyectos_ids:
        proyecto = proyecto_model.get_by_id(pid)
        if proyecto:
            proyectos.append(calcular_avance(proyecto))

    return proyectos
