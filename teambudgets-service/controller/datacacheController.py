from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
import json
import os, signal
from utils import serviceCache

router = APIRouter()

class KeyValuePayload(BaseModel):
    data: dict


@router.get("/data/{key}")
def read_data(key: str):
    value = serviceCache.get_data(key)
    if value is None:
        raise HTTPException(status_code=404, detail="Clave no encontrada")
    return {key: value}

@router.post("/data")
def write_data(payload: KeyValuePayload):
    serviceCache.set_data_bulk(payload.data)
    return {"message": "Datos guardados correctamente", "saved": payload.data}