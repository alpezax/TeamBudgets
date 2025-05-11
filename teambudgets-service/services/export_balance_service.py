import os
import json
import traceback
from pathlib import Path
from bson import ObjectId
from model.document import Document
from reports.generar_pdf_balance import generar_pdf_balance
from services.horasImputadasAProyectoService import ImputacionesAproyectoService

def exportar_balance_pdf(presupuesto_id: str, nombre_reporte: str = None, carpeta_salida: str = "reports"):
    """
    Exporta un documento de la colección 'presupuestos' a un PDF.

    :param presupuesto_id: ID del documento de presupuesto.
    :param nombre_reporte: Nombre opcional del archivo PDF (sin extensión).
    :param carpeta_salida: Carpeta donde se guardará el PDF.
    :return: Ruta completa del archivo PDF generado.
    """
    try:
        doc = Document(collection_name="presupuestos", document_filter={"_id": ObjectId(presupuesto_id)})
        data = doc.get_document()

        if not data:
            raise ValueError(f"No se encontró un documento con ID {presupuesto_id}.")

        nombre_archivo = nombre_reporte or f"balance_{presupuesto_id}"
        Path(carpeta_salida).mkdir(parents=True, exist_ok=True)
        ruta_pdf = os.path.join(carpeta_salida, f"{nombre_archivo}.pdf")

        # Obtenemos el resto
        impus = ImputacionesAproyectoService(presupuesto_id)
        data['imputaciones-persona'] = impus.get_imputaciones()

        generar_pdf_balance(data, ruta_pdf)

        return ruta_pdf

    except Exception as e:
        # Imprimir el stack trace completo del error
        print("Se ha producido un error al exportar el PDF del balance:")
        print(traceback.format_exc())
        
        # Volver a lanzar el error con un mensaje detallado
        raise RuntimeError(f"Error al exportar el PDF del balance: {str(e)}")
