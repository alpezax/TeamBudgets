import os
import json
import traceback
from pathlib import Path
from bson import ObjectId
from model.document import Document
from model.equipo import Equipo
from model.proyecto import Proyecto
from reports.generar_pdf_balance import generar_pdf_balance
from services.horasImputadasAProyectoService import ImputacionesAproyectoService

import json

def _calcular_horas(proyectodict):
    # Paso 1: Obtener las transacciones ordenadas si existen y no están vacías
    tx_list = proyectodict.get("tx", [])
    tx_sorted = sorted(tx_list, key=lambda tx: tx["timestamp"]) if tx_list else []

    # Paso 2: Calcular horas iniciales
    horas_disponibles = proyectodict["horas"]["venta"] * (1 - proyectodict["margen-contrato"]["margen"])

    # Paso 3: Si no hay transacciones, devolver entrada por defecto
    if not tx_sorted:
        return [{
            "mes_str": "",
            "horas": 0,
            "input_horas": round(horas_disponibles, 2),
            "output_horas": round(horas_disponibles, 2)
        }]

    # Paso 4: Procesar transacciones
    resultados = []
    for tx in tx_sorted:
        input_horas = horas_disponibles
        output_horas = input_horas - tx["horas"]

        resultados.append({
            "mes_str": tx["mes_str"],
            "horas": tx["horas"],
            "input_horas": round(input_horas, 2),
            "output_horas": round(output_horas, 2)
        })

        horas_disponibles = output_horas
    return resultados


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

        # Obtenemos los proyectos con los que cuenta el equipo
        equipo = Equipo()
        proyecto = Proyecto()
        proyectos=[]
        for proyecto_id in equipo.get_proyectos_by_id(data['equipo']['id']):
            prox=proyecto.get_by_id(proyecto_id)
            prox['calculo-horas']=_calcular_horas(prox)
            proyectos.append(prox)
        data['estado-proyectos'] = proyectos
        
        generar_pdf_balance(data, ruta_pdf)
        return ruta_pdf

    except Exception as e:
        # Imprimir el stack trace completo del error
        print("Se ha producido un error al exportar el PDF del balance:")
        print(traceback.format_exc())
        
        # Volver a lanzar el error con un mensaje detallado
        raise RuntimeError(f"Error al exportar el PDF del balance: {str(e)}")
