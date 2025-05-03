from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, ConfigDict
from typing import Dict, Optional, Any
from bson.errors import InvalidId
from bson.objectid import ObjectId
from utils.objectid_to_str import objectid_to_str
from model.document import Document


router = APIRouter()

class SetFieldRequest(BaseModel):
    path: str
    value: Any

    model_config = ConfigDict(arbitrary_types_allowed=True)

class UpdateRequest(BaseModel):
    updates: Dict[str, Any]

    model_config = ConfigDict(arbitrary_types_allowed=True)

class DeleteFieldRequest(BaseModel):
    path: str

class CreateRequest(BaseModel):
    data: Optional[Dict] = {}

@router.get("/document/{collection_name}")
def get_document(collection_name: str, id: Optional[str] = None):
    try:
        doc_filter = {"_id": ObjectId(id)} if id else {}
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID no válido")

    document = Document(collection_name, doc_filter)
    return document.get_document()

@router.get("/document/{collection_name}/field")
def get_field(collection_name: str, path: str, id: Optional[str] = None):
    try:
        doc_filter = {"_id": ObjectId(id)} if id else {}
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID no válido")

    document = Document(collection_name, doc_filter)
    value = document.get(path)
    if value is None:
        raise HTTPException(status_code=404, detail="Campo no encontrado")
    return {path: value}

@router.post("/document/{collection_name}/field")
def set_field(collection_name: str, body: SetFieldRequest, id: Optional[str] = None):
    try:
        doc_filter = {"_id": ObjectId(id)} if id else {}
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID no válido")

    document = Document(collection_name, doc_filter)
    document.set(body.path, body.value)
    return {"message": f"Campo '{body.path}' actualizado."}

@router.put("/document/{collection_name}")
def update_fields(collection_name: str, body: UpdateRequest, id: Optional[str] = None):
    try:
        doc_filter = {"_id": ObjectId(id)} if id else {}
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID no válido")

    document = Document(collection_name, doc_filter)
    document.update(body.updates)
    return {"message": "Documento actualizado."}

@router.delete("/document/{collection_name}/field")
def delete_field(collection_name: str, body: DeleteFieldRequest, id: Optional[str] = None):
    try:
        doc_filter = {"_id": ObjectId(id)} if id else {}
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID no válido")

    document = Document(collection_name, doc_filter)
    document.delete_field(body.path)
    return {"message": f"Campo '{body.path}' eliminado."}

@router.delete("/document/{collection_name}")
def delete_document(collection_name: str, id: Optional[str] = None):
    try:
        doc_filter = {"_id": ObjectId(id)} if id else {}
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID no válido")

    document = Document(collection_name, doc_filter)
    document.delete_document()
    return {"message": "Documento eliminado."}



@router.post("/document/{collection_name}")
def create_document(collection_name: str, body: CreateRequest):
    """
    Crea un nuevo documento en la colección utilizando la clase Document.
    """
    document = Document(collection_name)
    inserted_id = document.create(body.data)  # Método que devuelve el ObjectId
    
    # Crear la respuesta y convertir ObjectId a string
    response_data = {
        "message": "Documento creado.",
        "id": inserted_id,  # ObjectId se convertirá en string
        "data": body.data
    }

    # Convertir cualquier ObjectId en la respuesta a string
    return objectid_to_str(response_data)