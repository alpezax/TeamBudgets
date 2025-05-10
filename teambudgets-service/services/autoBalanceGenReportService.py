import os
import logging
from services.autoBalanceService import calcular_balance_equipo
from reports.autoBalanceReportTemplate import generar_pdf


def generar_informe_balance(
    equipo_id: str,
    yyyy_mm: str,
    nombre_reporte: str = None,
    carpeta_salida: str = "reports"
) -> dict:
    """
    Calcula el balance de un equipo para un mes determinado y genera un informe PDF.

    Args:
        equipo_id (str): ID del equipo a balancear.
        yyyy_mm (str): Mes en formato 'YYYY-MM'.
        nombre_reporte (str, optional): Nombre del archivo PDF a generar. Se genera automáticamente si no se especifica.
        carpeta_salida (str, optional): Carpeta donde se guardará el PDF. Por defecto, 'reports'.

    Returns:
        dict: Resultado del proceso con status, logs e información del archivo generado (si aplica).
    """
    resultado = calcular_balance_equipo(equipo_id, yyyy_mm)

    if resultado["status"] == "KO":
        logging.error(f"No se pudo generar el informe de balance para el equipo {equipo_id} en {yyyy_mm}")
        return resultado

    try:
        # Definir nombre del archivo
        if not nombre_reporte:
            nombre_reporte = f"informe_balance_{equipo_id}_{yyyy_mm}.pdf"

        # Asegurar que la carpeta existe
        os.makedirs(carpeta_salida, exist_ok=True)

        # Construir el path completo
        path_archivo = os.path.join(carpeta_salida, nombre_reporte)

        # Generar el PDF en la ubicación deseada
        generar_pdf(resultado, path_archivo)

        resultado["archivo"] = path_archivo
        logging.info(f"Informe PDF generado correctamente en {path_archivo}")

    except Exception as e:
        logging.exception("Error generando el informe PDF")
        resultado["logs"].append(str(e))

    return resultado
