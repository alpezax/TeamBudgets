from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from services.autoBalanceService import calcular_balance_equipo  
from datetime import date

router = APIRouter(prefix="/equipo", tags=["Equipo"])



@router.get("/autobalance/{id}/{yyyy_mm}")
async def obtener_balance(id: str, yyyy_mm: str):
    try:
        # Llamamos al método calcular_balance_equipo del AutoBalanceService
         return calcular_balance_equipo(id, yyyy_mm)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
