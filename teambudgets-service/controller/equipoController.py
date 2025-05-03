from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from model.equipo import Equipo

router = APIRouter(prefix="/equipo", tags=["Equipo"])
equipo_model = Equipo()

class EquipoCreate(BaseModel):
    nombre: str
    descripcion: str

class MiembroInput(BaseModel):
    trabajador_id: str = Field(..., description="ID del trabajador")
    participacion: float = Field(..., ge=0, le=100, description="Porcentaje de participación")
    nombre: str

class EquipoCreateInput(BaseModel):
    nombre: str
    miembros: Optional[List[MiembroInput]] = []


class EquipoUpdateInput(BaseModel):
    nombre: Optional[str] = None
    miembros: Optional[List[MiembroInput]] = None


@router.get("/")
def get_all_equipos():
    equipo_model = Equipo()
    return equipo_model.get_all()


@router.get("/{id}")
def get_equipo_by_id(id: str):
    equipo_model = Equipo()
    result = equipo_model.get_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return result


@router.post("/")
def crear_equipo(equipo: EquipoCreate):
    equipo_model = Equipo()
    equipo_id = equipo_model.create(nombre=equipo.nombre, descripcion=equipo.descripcion)
    return {"id": equipo_id}


@router.put("/{id}")
def update_equipo(id: str, data: EquipoUpdateInput):
    equipo_model = Equipo()
    updated = equipo_model.update(id_str=id, nombre=data.nombre, miembros=data.miembros)
    if not updated:
        raise HTTPException(status_code=404, detail="Equipo no encontrado o sin cambios")
    return {"message": "Equipo actualizado correctamente"}


@router.delete("/{id}")
def delete_equipo(id: str):
    equipo_model = Equipo()
    deleted = equipo_model.delete(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return {"message": "Equipo eliminado correctamente"}


@router.post("/{equipo_id}/miembro/")
def añadir_miembro_equipo(equipo_id: str, miembro: MiembroInput):
    """
    Agrega un nuevo miembro a un equipo.
    :param equipo_id: ID del equipo.
    :param miembro: Diccionario con 'trabajador_id' y 'participacion'.
    """
    equipo_model = Equipo()
    success = equipo_model.add_miembro(
        equipo_id=equipo_id,
        trabajador_id=miembro.trabajador_id,
        participacion=miembro.participacion,
        nombre= miembro.nombre
    )
    if success:
        return {"message": "Miembro añadido exitosamente"}
    else:
        raise HTTPException(status_code=400, detail="No se pudo añadir el miembro al equipo")

@router.put("/{id}/miembro")
def actualizar_participacion_miembro(id: str, miembro: MiembroInput):
    equipo_model = Equipo()
    actualizado = equipo_model.actualizar_participacion_miembro(
        equipo_id=id,
        trabajador_id=miembro.trabajador_id,
        participacion=miembro.participacion
    )
    if not actualizado:
        raise HTTPException(status_code=404, detail="Miembro o equipo no encontrado o ya actualizado. Revise si se ha actualizado")
    return {"message": "Participación actualizada correctamente"}