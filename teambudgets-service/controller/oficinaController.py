from fastapi import APIRouter, HTTPException
from model.oficina import Oficina
from pydantic import BaseModel

router = APIRouter()
oficina_model = Oficina()


@router.get("/oficina/")
def get_all_oficinas():
    print("Listando oficinas")
    oficina_model = Oficina()
    return oficina_model.get_all()


@router.get("/oficina/{id}")
def get_oficina_by_id(id: str):
    oficina_model = Oficina()
    doc = oficina_model.get_by_id(id)
    if not doc:
        raise HTTPException(status_code=404, detail="Oficina no encontrada")
    return doc


class OficintaCreate(BaseModel):
    ciudad: str
    tipo: str
    simbolo: str
    
@router.post("/oficina/")
def create_oficina(oficinaCreate : OficintaCreate):
    oficina_model = Oficina()
    return {"id": oficina_model.create(oficinaCreate.ciudad, oficinaCreate.tipo, oficinaCreate.simbolo)}


@router.put("/oficina/{id}")
def update_oficina(id,oficinaCreate : OficintaCreate):
    oficina_model = Oficina()
    updated = oficina_model.update(id, oficinaCreate.ciudad, oficinaCreate.tipo, oficinaCreate.simbolo)
    if not updated:
        raise HTTPException(status_code=404, detail="Oficina no encontrada o sin cambios")
    return {"message": "Actualizado correctamente"}


@router.delete("/oficina/{id}")
def delete_oficina(id: str):
    oficina_model = Oficina()
    deleted = oficina_model.delete(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Oficina no encontrada")
    return {"message": "Eliminada correctamente"}


@router.get("/oficina/{id}/dias-laborables/{yyyy_mm}")
def get_dias_laborables(id: str, yyyy_mm: str):
    oficina_model = Oficina()
    valor = oficina_model.get_dias_laborables(id, yyyy_mm)
    if valor is None:
        raise HTTPException(status_code=404, detail="Datos no encontrados")
    return {yyyy_mm: valor}


@router.put("/oficina/{id}/dias-laborables/{yyyy_mm}")
def set_dias_laborables(id: str, yyyy_mm: str, valor: int):
    oficina_model = Oficina()
    success = oficina_model.set_dias_laborables(id, yyyy_mm, valor)
    if not success:
        raise HTTPException(status_code=404, detail="Oficina no encontrada")
    return {"message": f"Días laborables para {yyyy_mm} actualizados a {valor}"}


@router.get("/oficina/simbolo/{simbolo}")
def get_oficina_por_simbolo(simbolo: str):
    oficina_model = Oficina()
    doc = oficina_model.get_oficina_por_simbolo(simbolo)
    if not doc:
        raise HTTPException(status_code=404, detail="Oficina no encontrada")
    return doc


@router.get("/oficina/simbolo/{simbolo}/ultima-fecha-laborable")
def get_ultima_fecha_laborable_por_simbolo(simbolo: str):
    oficina_model = Oficina()
    data = oficina_model.get_ultima_fecha_laborable_por_simbolo(simbolo)
    if not data:
        raise HTTPException(status_code=404, detail="No se encontraron fechas")
    return data
