from db.mongo_connection import getDb
from bson import ObjectId


class Proyecto:
    def __init__(self):
        self.collection = getDb()["proyectos"]

    def _to_dict(self, doc):
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    def get_all(self):
        return [self._to_dict(doc) for doc in self.collection.find()]

    def get_by_id(self, id_str: str):
        try:
            doc = self.collection.find_one({"_id": ObjectId(id_str)})
            return self._to_dict(doc)
        except Exception:
            return None

    def create(self, nombre: str, idext: str, descripcion: str, horas: dict = None, margen_contrato: dict = None):
        new_doc = {
            "nombre": nombre,
            "idext": idext,
            "descripcion": descripcion,
            "horas": horas or {"venta": 0, "consumidas": 0},
            "margen-contrato": margen_contrato or {}
        }
        result = self.collection.insert_one(new_doc)
        return str(result.inserted_id)

    def update(self, id_str: str, nombre: str = None, idext: str = None, descripcion: str = None, horas: dict = None):
        update_fields = {}
        if nombre is not None:
            update_fields["nombre"] = nombre
        if idext is not None:
            update_fields["idext"] = idext
        if descripcion is not None:
            update_fields["descripcion"] = descripcion
        if horas is not None:
            update_fields["horas"] = horas

        result = self.collection.update_one(
            {"_id": ObjectId(id_str)},
            {"$set": update_fields}
        )
        return result.modified_count > 0

    def get_horas(self, id_str: str):
        doc = self.get_by_id(id_str)
        if doc and "horas" in doc:
            return doc["horas"]
        return None

    def set_horas(self, id_str: str, horas: dict):
        result = self.collection.update_one(
            {"_id": ObjectId(id_str)},
            {"$set": {"horas": horas}}
        )
        return result.modified_count > 0

    def get_margen_contrato(self, id_str: str, yyyy_mm: str):
        doc = self.get_by_id(id_str)
        if doc and "margen-contrato" in doc:
            return doc["margen-contrato"].get(yyyy_mm)
        return None

    def set_margen_contrato(self, id_str: str, yyyy_mm: str, valor: float):
        result = self.collection.update_one(
            {"_id": ObjectId(id_str)},
            {"$set": {f"margen-contrato.{yyyy_mm}": valor}}
        )
        return result.modified_count > 0

    def delete(self, id_str: str):
        result = self.collection.delete_one({"_id": ObjectId(id_str)})
        return result.deleted_count > 0
