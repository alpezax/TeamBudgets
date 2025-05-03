from fastapi import APIRouter, HTTPException
from model.constantes import Constantes
from model.constantesList import ConstantesList
from pydantic import BaseModel
from typing import Dict
from utils import objectid_to_str 

router = APIRouter()

# Instancia de las clases
constantes_handler = Constantes()
constantes_list_handler = ConstantesList()

# Modelos para Pydantic (Para validación de datos de entrada)
class TarifaRequest(BaseModel):
    fecha: str
    valor: float

# Rutas del controlador

@router.get("/constantes")
def get_constantes():
    """
    Obtiene todas las constantes.
    """
    constantes_handler = Constantes()
    constantes_list_handler = ConstantesList()
    constantes = constantes_list_handler.get_all_constantes()
    # Convierte los ObjectId a string antes de devolver la respuesta
    return objectid_to_str.objectid_to_str(constantes)

@router.get("/constantes/horas-jornada")
def get_horas_jornada():
    """
    Obtiene las horas de jornada configuradas.
    """
    constantes_handler = Constantes()
    constantes_list_handler = ConstantesList()
    horas_jornada = constantes_handler.get_horas_jornada()
    return objectid_to_str.objectid_to_str({"horas-jornada": horas_jornada})

@router.post("/constantes/horas-jornada")
def set_horas_jornada(horas: int):
    """
    Actualiza las horas de jornada configuradas.
    """
    constantes_handler = Constantes()
    constantes_list_handler = ConstantesList()
    constantes_handler.set_horas_jornada(horas)
    return objectid_to_str.objectid_to_str({"message": "Horas de jornada actualizadas con éxito"})

@router.get("/constantes/tarifa/{yyyy_mm}")
def get_tarifa(yyyy_mm: str):
    """
    Obtiene la tarifa de un mes específico (YYYY-MM).
    """
    constantes_handler = Constantes()
    constantes_list_handler = ConstantesList()
    tarifa = constantes_handler.get_tarifa(yyyy_mm)
    if tarifa is None:
        raise HTTPException(status_code=404, detail="Tarifa no encontrada")
    return objectid_to_str.objectid_to_str({"tarifa": tarifa})

@router.post("/constantes/tarifa")
def set_tarifa(tarifa: TarifaRequest):
    """
    Establece una tarifa para un mes específico (YYYY-MM).
    """
    constantes_handler = Constantes()
    constantes_list_handler = ConstantesList()
    constantes_handler.set_tarifa(tarifa.fecha, tarifa.valor)
    return objectid_to_str.objectid_to_str({"message": f"Tarifa para {tarifa.fecha} actualizada con éxito"})

@router.get("/constantes/ultima-tarifa")
def get_ultima_tarifa():
    """
    Obtiene la última tarifa (la más reciente).
    """
    constantes_handler = Constantes()
    constantes_list_handler = ConstantesList()
    tarifa = constantes_handler.get_ultima_tarifa()
    if tarifa is None:
        raise HTTPException(status_code=404, detail="No hay tarifas registradas")
    return objectid_to_str.objectid_to_str(tarifa)

@router.get("/constantes/tarifa-cercana/{yyyy_mm}")
def get_tarifa_cercana(yyyy_mm: str):
    """
    Obtiene la tarifa más cercana al mes especificado (YYYY-MM).
    """
    constantes_handler = Constantes()
    constantes_list_handler = ConstantesList()    
    tarifa = constantes_handler.get_tarifa_mas_cercana(yyyy_mm)
    if tarifa is None:
        raise HTTPException(status_code=404, detail="No hay tarifas para la fecha solicitada")
    return objectid_to_str.objectid_to_str(tarifa)
