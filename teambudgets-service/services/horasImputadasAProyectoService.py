from db.mongo_connection import getDb
from bson.objectid import ObjectId
from typing import Dict, Any
from bson import ObjectId

class ImputacionesAproyectoService:
    def __init__(self, document_id: str):
        self.collection = getDb()["presupuestos"]
        self.document_id = ObjectId(document_id)
        self.document = self._load_document()

    def _load_document(self) -> Dict[str, Any]:
        """Carga el documento por ID desde la colección de presupuestos."""
        document = self.collection.find_one({"_id": self.document_id})
        if not document:
            raise ValueError(f"Documento con ID {self.document_id} no encontrado.")
        return document

    def get_imputaciones(self) -> Dict[str, Dict[str, float]]:
        """
        Devuelve un diccionario donde cada trabajador tiene un mapeo de su `idext` asociado
        y las horas imputadas en ese proyecto.
        """
        imputaciones = self.document.get("imputaciones", [])
        result = {}

        for imputacion in imputaciones:
            idext = imputacion.get("idext")
            if not idext:
                continue  # Si no tiene idext, se salta esta imputación

            for gasto in imputacion.get("gastos", []):
                nombre = gasto.get("nombre")
                horas = gasto.get("horas")

                if nombre and horas:
                    if nombre not in result:
                        result[nombre] = {}

                    # Si ya existe una entrada para este idext, sumamos las horas
                    if idext in result[nombre]:
                        result[nombre][idext] += horas
                    else:
                        result[nombre][idext] = horas

        return result