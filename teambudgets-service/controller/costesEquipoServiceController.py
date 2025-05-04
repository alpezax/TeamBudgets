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

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from services.costesEquipoService import calcular_coste_equipo_por_mes, forecast_coste_equipo
from utils import objectid_to_str

router = APIRouter()

class CosteEquipoRequest(BaseModel):
    equipo_id: str
    fecha: str  # formato: 'YYYY-MM'

class ForecastCosteEquipoRequest(BaseModel):
    equipo_id: str
    fecha_inicio: str  # formato: 'YYYY-MM'
    n_meses: int

@router.post("/equipo/coste-mensual", response_model=Dict[str, Any])
def get_coste_equipo_mensual(payload: CosteEquipoRequest):
    try:
        resultado = calcular_coste_equipo_por_mes(payload.equipo_id, payload.fecha)
        if "error" in resultado:
            raise HTTPException(status_code=404, detail=resultado["error"])
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/equipo/forecast-coste", response_model=List[Dict[str, Any]])
def get_forecast_coste_equipo(payload: ForecastCosteEquipoRequest):
    try:
        resultados = forecast_coste_equipo(payload.equipo_id, payload.fecha_inicio, payload.n_meses)
        return resultados
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
