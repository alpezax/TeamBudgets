from bson import ObjectId
from model.document import Document
from model.proyecto import Proyecto


def apply_budget(presupuesto_id: str):
    # Cargar el presupuesto desde la colección 'presupuestos'
    doc = Document("presupuestos", {"_id": ObjectId(presupuesto_id)})
    presupuesto = doc.get_document()

    if not presupuesto:
        raise ValueError(f"No se encontró ningún presupuesto con id {presupuesto_id}")

    imputaciones = presupuesto.get("imputaciones", [])
    nombre_presupuesto = presupuesto.get("nombre_balance", "Sin nombre")
    mes_str = presupuesto.get("mes_anyo_str", "0000-00")  # formato YYYY-MM

    proyecto_service = Proyecto()

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
            mes_str=mes_str
        )

        if success:
            print(f"Transacción aplicada al proyecto {proyecto_id}")
            return success 
        else:
            print(f"Error aplicando transacción al proyecto {proyecto_id}")
            return False