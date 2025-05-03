from fastapi import APIRouter, HTTPException
from model.categoriaTrabajador import CategoriaTrabajador
from pydantic import BaseModel

router = APIRouter(prefix="/categoria-trabajador", tags=["Categoria Trabajador"])
categoria_model = CategoriaTrabajador()


@router.get("/")
def get_all_categorias():
    categoria_model = CategoriaTrabajador()
    return categoria_model.get_all()


@router.get("/{id}")
def get_categoria_by_id(id: str):
    categoria_model = CategoriaTrabajador()
    result = categoria_model.get_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return result


@router.get("/simbolo/{simbolo}")
def get_categoria_by_simbolo(simbolo: str):
    categoria_model = CategoriaTrabajador()
    result = categoria_model.get_categoria_por_simbolo(simbolo)
    if not result:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return result


@router.get("/csr/{simbolo}/ultimo")
def get_ultimo_csr(simbolo: str):
    categoria_model = CategoriaTrabajador()
    result = categoria_model.get_ultimo_csr_por_simbolo(simbolo)
    if not result:
        raise HTTPException(status_code=404, detail="No se encontró CSR para ese símbolo")
    return result


@router.get("/csr/{id}/{yyyy_mm}")
def get_csr_by_fecha(id: str, yyyy_mm: str):
    categoria_model = CategoriaTrabajador()
    result = categoria_model.get_csr(id, yyyy_mm)
    if result is None:
        raise HTTPException(status_code=404, detail="CSR no encontrado para la fecha")
    return {yyyy_mm: result}


class CategoriaCreate(BaseModel):
    nombre: str
    clase: str
    simbolo: str
    
@router.post("/")
def crear_categoria(categoria: CategoriaCreate):
    categoria_model = CategoriaTrabajador()
    new_id = categoria_model.create(categoria.nombre, categoria.clase, categoria.simbolo)
    return {"id": new_id}


@router.put("/{id}")
def actualizar_categoria(id: str, nombre: str = None, clase: str = None, simbolo: str = None):
    categoria_model = CategoriaTrabajador()
    updated = categoria_model.update(id, nombre, clase, simbolo)
    if not updated:
        raise HTTPException(status_code=404, detail="Categoría no actualizada")
    return {"message": "Categoría actualizada correctamente"}

class ValorCsr(BaseModel):
    valor: float

@router.put("/csr/{id}/{yyyy_mm}")
def actualizar_csr(id: str, yyyy_mm: str, valor: ValorCsr):
    categoria_model = CategoriaTrabajador()
    updated = categoria_model.set_csr(id, yyyy_mm, valor.valor)
    if not updated:
        raise HTTPException(status_code=404, detail="CSR no actualizado")
    return {"message": f"CSR actualizado para {yyyy_mm}"}


@router.delete("/{id}")
def eliminar_categoria(id: str):
    categoria_model = CategoriaTrabajador()
    deleted = categoria_model.delete(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Categoría no eliminada")
    return {"message": "Categoría eliminada correctamente"}
