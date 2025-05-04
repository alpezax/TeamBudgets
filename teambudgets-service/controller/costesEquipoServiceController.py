from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from services.costesEquipoService import calcular_coste_equipo_por_mes 
from utils import objectid_to_str

router = APIRouter()

class CosteEquipoRequest(BaseModel):
    equipo_id: str
    fecha: str  # formato: 'YYYY-MM'

@router.post("/equipo/coste-mensual", response_model=Dict[str, Any])
def get_coste_equipo_mensual(payload: CosteEquipoRequest):
    try:
        resultado = calcular_coste_equipo_por_mes(payload.equipo_id, payload.fecha)
        if "error" in resultado:
            raise HTTPException(status_code=404, detail=resultado["error"])
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
