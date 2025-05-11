from bson import ObjectId
from model.document import Document
from model.proyecto import Proyecto
import uuid

def apply_budget(presupuesto_id: str) -> bool:
    # Cargar el presupuesto desde la colección 'presupuestos'
    doc = Document("presupuestos", {"_id": ObjectId(presupuesto_id)})
    presupuesto = doc.get_document()

    if not presupuesto:
        raise ValueError(f"No se encontró ningún presupuesto con id {presupuesto_id}")

    imputaciones = presupuesto.get("imputaciones", [])
    nombre_presupuesto = presupuesto.get("nombre_balance", "Sin nombre")
    mes_str = presupuesto.get("mes_anyo_str", "0000-00")  # formato YYYY-MM

    proyecto_service = Proyecto()
    txid=str(uuid.uuid4())
    
    for imputacion in imputaciones:
        proyecto_id = imputacion.get("proyecto_id")
        horas = imputacion.get("horas")

        if not proyecto_id or horas is None:
            print("Imputación incompleta, se ignora.")
            continue
        
        success = proyecto_service.aplica_transaccion(
            id_proyecto=proyecto_id,
            horas=horas,
            presupuesto_id=presupuesto_id,
            presupuesto_nombre=nombre_presupuesto,
            mes_str=mes_str,
            txid=txid
        )
        
        doc.set_or_create_field("txid",txid)
        
        if not success:
            print(f"Error aplicando transacción al proyecto {proyecto_id}")
            return False  # Si falla una transacción, se interrumpe

        print(f"Transacción aplicada al proyecto {proyecto_id}")

    return True  # Solo si todas fueron exitosas

def apply_budget_rollback(presupuesto_id: str) -> bool:
    # Cargar el presupuesto desde la colección 'presupuestos'
    doc = Document("presupuestos", {"_id": ObjectId(presupuesto_id)})
    presupuesto = doc.get_document()

    if not presupuesto:
        raise ValueError(f"No se encontró ningún presupuesto con id {presupuesto_id}")
    
    txid = presupuesto.get("txid")
    if not txid:
        raise ValueError(f"El presupuesto con id {presupuesto_id} no tiene un txid asociado para rollback")

    imputaciones = presupuesto.get("imputaciones", [])
    proyecto_service = Proyecto()

    for imputacion in imputaciones:
        proyecto_id = imputacion.get("proyecto_id")
        if not proyecto_id:
            print("Imputación incompleta, falta proyecto_id. Se ignora.")
            continue

        success = proyecto_service.rollback_transaccion(proyecto_id, txid)
        if not success:
            print(f"Error al revertir transacción en proyecto {proyecto_id}")
            return False  # Se interrumpe si falla un rollback

        print(f"Rollback realizado para proyecto {proyecto_id}")

    return True
