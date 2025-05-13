from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional, List
from model.proyecto import Proyecto
from services import proyectoService 

router = APIRouter()
proyecto_model = Proyecto()


# Modelo base para la creación de un proyecto
class ProyectoBase(BaseModel):
    nombre: str
    idext: str
    descripcion: str
    horas: Optional[Dict[str, int]] = {"venta": 0, "consumidas": 0}
    margen_contrato: Optional[Dict[str, float]] = {}
    workpool: Optional[List[str]] = []  # Lista de IDs de trabajadores asignados al proyecto
    tarifa_hora: Optional[float] = None  


# Modelo para la actualización parcial de un proyecto
class ProyectoUpdate(BaseModel):
    nombre: Optional[str] = None
    idext: Optional[str] = None
    descripcion: Optional[str] = None
    horas: Optional[Dict[str, int]] = None
    margen_contrato: Optional[Dict[str, float]] = None
    workpool: Optional[List[str]] = None
    tarifa_hora: Optional[float] = None  


# Endpoint para crear un nuevo proyecto
@router.post("/proyecto/", response_model=str)
async def create_proyecto(proyecto: ProyectoBase):
    proyecto_model = Proyecto()
    proyecto_id = proyecto_model.create(
        proyecto.nombre,
        proyecto.idext,
        proyecto.descripcion,
        proyecto.horas,
        proyecto.margen_contrato,
        proyecto.tarifa_hora  
    )
    return proyecto_id


# Endpoint para obtener todos los proyectos
@router.get("/proyectos/", response_model=list)
async def get_all_proyectos():
    proyecto_model = Proyecto()
    return proyecto_model.get_all()


# Endpoint para obtener un proyecto por su ID
@router.get("/proyecto/{id_str}", response_model=ProyectoBase)
async def get_proyecto(id_str: str):
    proyecto_model = Proyecto()
    proyecto = proyecto_model.get_by_id(id_str)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto not found")
    return proyecto


# Endpoint para actualizar parcialmente un proyecto
@router.put("/proyecto/{id_str}", response_model=bool)
async def update_proyecto(id_str: str, proyecto: ProyectoUpdate):
    proyecto_model = Proyecto()
    updated = proyecto_model.update(
        id_str,
        nombre=proyecto.nombre,
        idext=proyecto.idext,
        descripcion=proyecto.descripcion,
        horas=proyecto.horas,
        workpool=proyecto.workpool,
        tarifa_hora=proyecto.tarifa_hora  
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Proyecto not found")
    return updated


# Endpoint para eliminar un proyecto por su ID
@router.delete("/proyecto/{id_str}", response_model=bool)
async def delete_proyecto(id_str: str):
    proyecto_model = Proyecto()
    deleted = proyecto_model.delete(id_str)
    if not deleted:
        raise HTTPException(status_code=404, detail="Proyecto not found")
    return deleted


# Endpoint para obtener las horas asociadas a un proyecto
@router.get("/proyecto/{id_str}/horas", response_model=Dict[str, int])
async def get_horas_proyecto(id_str: str):
    proyecto_model = Proyecto()
    horas = proyecto_model.get_horas(id_str)
    if not horas:
        raise HTTPException(status_code=404, detail="Horas not found")
    return horas


# Endpoint para actualizar las horas de un proyecto
@router.put("/proyecto/{id_str}/horas", response_model=bool)
async def set_horas_proyecto(id_str: str, horas: Dict[str, int]):
    proyecto_model = Proyecto()
    updated = proyecto_model.set_horas(id_str, horas)
    if not updated:
        raise HTTPException(status_code=404, detail="Proyecto not found")
    return updated


# Endpoint para obtener el margen de contrato de un proyecto en un mes específico
@router.get("/proyecto/{id_str}/margen-contrato/{yyyy_mm}", response_model=Optional[float])
async def get_margen_contrato(id_str: str, yyyy_mm: str):
    proyecto_model = Proyecto()
    margen = proyecto_model.get_margen_contrato(id_str, yyyy_mm)
    if margen is None:
        raise HTTPException(status_code=404, detail="Margen de contrato not found")
    return margen


# Endpoint para actualizar el margen de contrato de un proyecto en un mes específico
@router.put("/proyecto/{id_str}/margen-contrato/{yyyy_mm}", response_model=bool)
async def set_margen_contrato(id_str: str, yyyy_mm: str, valor: float):
    proyecto_model = Proyecto()
    updated = proyecto_model.set_margen_contrato(id_str, yyyy_mm, valor)
    if not updated:
        raise HTTPException(status_code=404, detail="Proyecto not found")
    return updated


# Endpoint para obtener la tarifa por hora de un proyecto
@router.get("/proyecto/{id_str}/tarifa-hora", response_model=Optional[float])
async def get_tarifa_hora(id_str: str):
    proyecto_model = Proyecto()
    tarifa = proyecto_model.get_tarifa_hora(id_str)
    if tarifa is None:
        raise HTTPException(status_code=404, detail="Tarifa-hora not found")
    return tarifa


# Endpoint para obtener todos los proyectos con el campo "avance"
@router.get("/proyectos/enriquecidos", response_model=list)
async def get_all_proyectos_con_avance():
    return proyectoService.get_all_proyectos()


# Endpoint para obtener los proyectos de un equipo con el campo "avance"
@router.get("/equipo/{equipo_id}/proyectos/enriquecidos", response_model=list)
async def get_proyectos_equipo_con_avance(equipo_id: str):
    return proyectoService.get_proyectos_de_equipo(equipo_id)