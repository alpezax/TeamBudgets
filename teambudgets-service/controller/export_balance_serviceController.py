from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from services.export_balance_service import exportar_balance_pdf
from services.horasImputadasAProyectoService import ImputacionesAproyectoService

router = APIRouter(prefix="/balance", tags=["Balance de Equipo"])


@router.get("/exportar-pdf")
def exportar_balance_controller(
    presupuesto_id: str = Query(..., description="ID del presupuesto en MongoDB"),
    nombre_reporte: Optional[str] = Query(None, description="Nombre del archivo PDF a generar"),
    carpeta_salida: Optional[str] = Query("reports", description="Carpeta donde se guardará el PDF")
):
    """
    Genera un informe PDF a partir de un documento de presupuesto.
    """
    try:
        ruta_pdf = exportar_balance_pdf(
            presupuesto_id=presupuesto_id,
            nombre_reporte=nombre_reporte,
            carpeta_salida=carpeta_salida
        )
        return {
            "mensaje": "PDF generado correctamente",
            "ruta_pdf": ruta_pdf
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/imputaciones")
def obtener_imputaciones_controller(
    presupuesto_id: str = Query(..., description="ID del presupuesto en MongoDB")
):
    """
    Obtiene las imputaciones de un proyecto a partir de un presupuesto.
    """
    try:
        service = ImputacionesAproyectoService(presupuesto_id)
        imputaciones = service.get_imputaciones()
        return {"imputaciones": imputaciones}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))