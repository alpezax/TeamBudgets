from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from model.trabajador import Trabajador
from utils.objectid_to_str import objectid_to_str

router = APIRouter()
trabajador_model = Trabajador()


class TrabajadorInput(BaseModel):
    nombre: str
    oficina: str
    categoria: str
    alias: str
    tags: Optional[List[str]] = []
    workpool: Optional[List[str]] = []
    dedicacion_mensual: Optional[Dict[str, Dict[str, int]]] = {}
    coste_hora_mensual: Optional[Dict[str, float]] = {}


class UpdateDedicacionInput(BaseModel):
    work: Optional[int] = 0
    vacation: Optional[int] = 0


@router.get("/trabajadores/")
def get_all_trabajadores():
    trabajador_model = Trabajador()
    return trabajador_model.get_all()


@router.get("/trabajador/{id_str}")
def get_trabajador(id_str: str):
    trabajador_model = Trabajador()
    trabajador = trabajador_model.get_by_id(id_str)
    if trabajador:
        return objectid_to_str(trabajador)
    raise HTTPException(status_code=404, detail="Trabajador no encontrado")


@router.get("/trabajador/alias/{alias}")
def get_trabajador_por_alias(alias: str):
    trabajador_model = Trabajador()
    trabajador = trabajador_model.get_by_alias(alias)
    if trabajador:
        return objectid_to_str(trabajador)
    raise HTTPException(status_code=404, detail="Trabajador no encontrado por alias")


@router.post("/trabajador/")
def create_trabajador(trabajador: TrabajadorInput):
    trabajador_model = Trabajador()
    return trabajador_model.create(
        trabajador.nombre,
        trabajador.oficina,
        trabajador.categoria,
        trabajador.alias,
        trabajador.tags,
        trabajador.workpool,
        trabajador.dedicacion_mensual,
        trabajador.coste_hora_mensual
    )


@router.put("/trabajador/{id_str}")
def update_trabajador(id_str: str, data: dict):
    trabajador_model = Trabajador()
    success = trabajador_model.update(id_str, **data)
    if not success:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado o sin cambios")
    return {"message": "Trabajador actualizado correctamente"}


@router.delete("/trabajador/{id_str}")
def delete_trabajador(id_str: str):
    trabajador_model = Trabajador()
    if trabajador_model.delete(id_str):
        return {"message": "Trabajador eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Trabajador no encontrado")


@router.get("/trabajador/{id_str}/dedicacion/{periodo}")
def get_dedicacion_mensual(id_str: str, periodo: str):
    trabajador_model = Trabajador()
    dedicacion = trabajador_model.get_dedicacion_mensual(id_str, periodo)
    if dedicacion:
        return dedicacion
    raise HTTPException(status_code=404, detail="Dedicación no encontrada para el mes especificado")


@router.put("/trabajador/{id_str}/dedicacion/{periodo}")
def set_dedicacion_mensual(id_str: str, periodo: str, data: UpdateDedicacionInput):
    trabajador_model = Trabajador()
    success = trabajador_model.set_dedicacion_mensual(id_str, periodo, data.dict())
    if not success:
        raise HTTPException(status_code=404, detail="No se pudo actualizar la dedicación")
    return {"message": "Dedicación actualizada correctamente"}


@router.get("/trabajador/{id_str}/coste/{yyyy_mm}")
def get_coste_hora_mensual(id_str: str, yyyy_mm: str):
    trabajador_model = Trabajador()
    coste = trabajador_model.get_coste_hora_mensual(id_str, yyyy_mm)
    if coste is not None:
        return {"coste_hora": coste}
    raise HTTPException(status_code=404, detail="Coste no encontrado para el mes especificado")


@router.put("/trabajador/{id_str}/coste/{yyyy_mm}")
def set_coste_hora_mensual(id_str: str, yyyy_mm: str, valor: float):
    trabajador_model = Trabajador()
    success = trabajador_model.set_coste_hora_mensual(id_str, yyyy_mm, valor)
    if not success:
        raise HTTPException(status_code=404, detail="No se pudo actualizar el coste-hora")
    return {"message": "Coste-hora actualizado correctamente"}


@router.get("/trabajadores/dedicacion/{yyyy_mm}")
def get_dedicaciones_por_mes(yyyy_mm: str):
    trabajador_model = Trabajador()
    return trabajador_model.get_dedicaciones_por_mes(yyyy_mm)


@router.get("/trabajadores/coste/{yyyy_mm}")
def get_costes_por_mes(yyyy_mm: str):
    trabajador_model = Trabajador()
    return trabajador_model.get_costes_por_mes(yyyy_mm)
