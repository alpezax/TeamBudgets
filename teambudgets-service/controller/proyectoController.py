from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
from model.proyecto import Proyecto

router = APIRouter()
proyecto_model = Proyecto()


class ProyectoBase(BaseModel):
    nombre: str
    idext: str
    descripcion: str
    horas: Optional[Dict[str, int]] = {"venta": 0, "consumidas": 0}
    margen_contrato: Optional[Dict[str, float]] = {}


class ProyectoUpdate(BaseModel):
    nombre: Optional[str] = None
    idext: Optional[str] = None
    descripcion: Optional[str] = None
    horas: Optional[Dict[str, int]] = None
    margen_contrato: Optional[Dict[str, float]] = None


@router.post("/proyecto/", response_model=str)
async def create_proyecto(proyecto: ProyectoBase):
    proyecto_model = Proyecto()
    proyecto_id = proyecto_model.create(
        proyecto.nombre,
        proyecto.idext,
        proyecto.descripcion,
        proyecto.horas,
        proyecto.margen_contrato
    )
    return proyecto_id


@router.get("/proyectos/", response_model=list)
async def get_all_proyectos():
    proyecto_model = Proyecto()
    return proyecto_model.get_all()


@router.get("/proyecto/{id_str}", response_model=ProyectoBase)
async def get_proyecto(id_str: str):
    proyecto_model = Proyecto()
    proyecto = proyecto_model.get_by_id(id_str)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto not found")
    return proyecto


@router.put("/proyecto/{id_str}", response_model=bool)
async def update_proyecto(id_str: str, proyecto: ProyectoUpdate):
    proyecto_model = Proyecto()
    updated = proyecto_model.update(
        id_str,
        nombre=proyecto.nombre,
        idext=proyecto.idext,
        descripcion=proyecto.descripcion,
        horas=proyecto.horas
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Proyecto not found")
    return updated


@router.delete("/proyecto/{id_str}", response_model=bool)
async def delete_proyecto(id_str: str):
    proyecto_model = Proyecto()
    deleted = proyecto_model.delete(id_str)
    if not deleted:
        raise HTTPException(status_code=404, detail="Proyecto not found")
    return deleted


@router.get("/proyecto/{id_str}/horas", response_model=Dict[str, int])
async def get_horas_proyecto(id_str: str):
    proyecto_model = Proyecto()
    horas = proyecto_model.get_horas(id_str)
    if not horas:
        raise HTTPException(status_code=404, detail="Horas not found")
    return horas


@router.put("/proyecto/{id_str}/horas", response_model=bool)
async def set_horas_proyecto(id_str: str, horas: Dict[str, int]):
    proyecto_model = Proyecto()
    updated = proyecto_model.set_horas(id_str, horas)
    if not updated:
        raise HTTPException(status_code=404, detail="Proyecto not found")
    return updated


@router.get("/proyecto/{id_str}/margen-contrato/{yyyy_mm}", response_model=Optional[float])
async def get_margen_contrato(id_str: str, yyyy_mm: str):
    proyecto_model = Proyecto()
    margen = proyecto_model.get_margen_contrato(id_str, yyyy_mm)
    if margen is None:
        raise HTTPException(status_code=404, detail="Margen de contrato not found")
    return margen


@router.put("/proyecto/{id_str}/margen-contrato/{yyyy_mm}", response_model=bool)
async def set_margen_contrato(id_str: str, yyyy_mm: str, valor: float):
    proyecto_model = Proyecto()
    updated = proyecto_model.set_margen_contrato(id_str, yyyy_mm, valor)
    if not updated:
        raise HTTPException(status_code=404, detail="Proyecto not found")
    return updated
