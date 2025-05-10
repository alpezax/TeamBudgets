from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from services.autoBalanceGenReportService import generar_informe_balance  
from typing import Optional

router = APIRouter(prefix="/balance", tags=["Balance de Equipo"])


class BalanceRequest(BaseModel):
    equipo_id: str
    yyyy_mm: str
    nombre_reporte: Optional[str] = None
    carpeta_salida: Optional[str] = "reports"


@router.post("/generar-informe")
def generar_informe_balance_equipo(request: BalanceRequest):
    resultado = generar_informe_balance(
        equipo_id=request.equipo_id,
        yyyy_mm=request.yyyy_mm,
        nombre_reporte=request.nombre_reporte,
        carpeta_salida=request.carpeta_salida
    )

    if resultado["status"] == "KO":
        raise HTTPException(status_code=400, detail={"logs": resultado.get("logs", [])})

    return {
        "status": "OK",
        "archivo": resultado.get("archivo"),
        "logs": resultado.get("logs", [])
    }
