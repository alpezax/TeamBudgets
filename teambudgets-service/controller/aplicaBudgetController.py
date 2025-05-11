from fastapi import APIRouter, HTTPException
from bson import ObjectId
from services.applyBudgetService import apply_budget
from model.presupuesto import Presupuesto
from services.validateBudgetService import ProyectoService

# Crear el router
router = APIRouter(prefix="/presupuestos", tags=["Presupuestos"])

# Instancias necesarias
presupuesto_model = Presupuesto()
proyectos_service = ProyectoService()


@router.post("/{presupuesto_id}/aplicar")
def aplicar_presupuesto(presupuesto_id: str):
    try:
        # Validar si el presupuesto existe
        presupuesto = presupuesto_model.collection.find_one({"_id": ObjectId(presupuesto_id)})
        if not presupuesto:
            raise HTTPException(status_code=404, detail="Presupuesto no encontrado")

        # Aplicar el presupuesto
        if apply_budget(presupuesto_id):

            # Marcar el presupuesto como ejecutado
            presupuesto_model.collection.update_one(
                {"_id": ObjectId(presupuesto_id)},
                {"$set": {"estado": "EXECUTED"}}
            )

            return {"mensaje": "Presupuesto aplicado y marcado como EXECUTED"}
        else: 
            return {"mensaje": "Error al aplicar el presupuesto"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al aplicar presupuesto: {e}")
