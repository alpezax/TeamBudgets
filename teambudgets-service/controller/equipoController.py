from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from model.equipo import Equipo

router = APIRouter(prefix="/equipo", tags=["Equipo"])
equipo_model = Equipo()


class MiembroInput(BaseModel):
    trabajador_id: str = Field(..., description="ID del trabajador")
    participacion: float = Field(..., ge=0, le=100, description="Porcentaje de participación")
    nombre: str


class EquipoCreateInput(BaseModel):
    nombre: str
    descripcion: Optional[str] = ""
    miembros: Optional[List[MiembroInput]] = []
    proyectos: Optional[List[str]] = []


class EquipoUpdateInput(BaseModel):
    nombre: Optional[str] = None
    miembros: Optional[List[MiembroInput]] = None
    proyectos: Optional[List[str]] = None


@router.get("/")
def get_all_equipos():
    return equipo_model.get_all()


@router.get("/{id}")
def get_equipo_by_id(id: str):
    result = equipo_model.get_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return result


@router.post("/")
def crear_equipo(equipo: EquipoCreateInput):
    equipo_id = equipo_model.create(
        nombre=equipo.nombre,
        descripcion=equipo.descripcion,
        miembros=equipo.miembros,
        proyectos=equipo.proyectos
    )
    return {"id": equipo_id}


@router.put("/{id}")
def update_equipo(id: str, data: EquipoUpdateInput):
    updated = equipo_model.update(
        id_str=id,
        nombre=data.nombre,
        miembros=data.miembros,
        proyectos=data.proyectos
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Equipo no encontrado o sin cambios")
    return {"message": "Equipo actualizado correctamente"}


@router.delete("/{id}")
def delete_equipo(id: str):
    deleted = equipo_model.delete(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return {"message": "Equipo eliminado correctamente"}


@router.post("/{equipo_id}/miembro/")
def añadir_miembro_equipo(equipo_id: str, miembro: MiembroInput):
    success = equipo_model.add_miembro(
        equipo_id=equipo_id,
        trabajador_id=miembro.trabajador_id,
        participacion=miembro.participacion,
        nombre=miembro.nombre
    )
    if success:
        return {"message": "Miembro añadido exitosamente"}
    else:
        raise HTTPException(status_code=400, detail="No se pudo añadir el miembro al equipo")


@router.put("/{id}/miembro")
def actualizar_participacion_miembro(id: str, miembro: MiembroInput):
    actualizado = equipo_model.actualizar_participacion_miembro(
        equipo_id=id,
        trabajador_id=miembro.trabajador_id,
        participacion=miembro.participacion
    )
    if not actualizado:
        raise HTTPException(status_code=404, detail="Miembro o equipo no encontrado o ya actualizado.")
    return {"message": "Participación actualizada correctamente"}


@router.post("/{equipo_id}/vincular_proyecto/{proyecto_id}")
def vincular_proyecto_equipo(equipo_id: str, proyecto_id: str):
    success = equipo_model.vincular_proyecto(equipo_id, proyecto_id)
    if not success:
        raise HTTPException(status_code=400, detail="No se pudo vincular el proyecto")
    return {"message": "Proyecto vinculado exitosamente"}


@router.delete("/{equipo_id}/desvincular_proyecto/{proyecto_id}")
def desvincular_proyecto_equipo(equipo_id: str, proyecto_id: str):
    success = equipo_model.desvincular_proyecto(equipo_id, proyecto_id)
    if not success:
        raise HTTPException(status_code=400, detail="No se pudo desvincular el proyecto")
    return {"message": "Proyecto desvinculado exitosamente"}
