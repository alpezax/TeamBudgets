from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from model.presupuesto import Presupuesto 
from services.validateBudgetService import BudgetValidationService, FullHoursImputedValidation, ProjectsHaveAvailableHoursValidation, ProyectoService


# Crear el router de FastAPI
router = APIRouter(prefix="/presupuestos", tags=["Presupuestos"])

# Crear las instancias necesarias
presupuesto_model = Presupuesto() 
proyectos_service = ProyectoService()
validation_rules = [
    FullHoursImputedValidation(),
    ProjectsHaveAvailableHoursValidation(proyectos_service)
]
validation_service = BudgetValidationService(presupuesto_model.collection, validation_rules)


class ValidationRequest(BaseModel):
    presupuesto_id: str

# Endpoints del controlador
@router.post("/validar")
async def validate_presupuesto(request: ValidationRequest):
    try:
        # Validamos el presupuesto utilizando el servicio
        resultado = validation_service.validate_presupuesto(request.presupuesto_id)
        return resultado
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoints del controlador
@router.post("/validarupdate")
async def validate_presupuesto(request: ValidationRequest):
    try:
        # Validamos el presupuesto utilizando el servicio y updateamos el resultado
        resultado = validation_service.validate_and_update(request.presupuesto_id)
        return resultado
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
