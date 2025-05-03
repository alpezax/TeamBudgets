from db.mongo_connection import getDb
from bson import ObjectId


class Oficina:
    def __init__(self):
        print("Iniciando")
        self.collection = getDb()["oficinas"]

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

    def create(self, ciudad: str, tipo: str, simbolo: str, dias_laborables: dict = None):
        new_doc = {
            "ciudad": ciudad,
            "tipo": tipo,
            "simbolo": simbolo,
            "dias-laborables": dias_laborables or {}
        }
        result = self.collection.insert_one(new_doc)
        return str(result.inserted_id)

    def update(self, id_str: str, ciudad: str = None, tipo: str = None, simbolo: str = None):
        update_fields = {}
        if ciudad is not None:
            update_fields["ciudad"] = ciudad
        if tipo is not None:
            update_fields["tipo"] = tipo
        if simbolo is not None:
            update_fields["simbolo"] = simbolo

        result = self.collection.update_one(
            {"_id": ObjectId(id_str)},
            {"$set": update_fields}
        )
        return result.modified_count > 0

    def delete(self, id_str: str):
        result = self.collection.delete_one({"_id": ObjectId(id_str)})
        return result.deleted_count > 0

    def get_dias_laborables(self, id_str: str, yyyy_mm: str):
        doc = self.get_by_id(id_str)
        if doc and "dias-laborables" in doc:
            return doc["dias-laborables"].get(yyyy_mm)
        return None

    def set_dias_laborables(self, id_str: str, yyyy_mm: str, valor: int):
        result = self.collection.update_one(
            {"_id": ObjectId(id_str)},
            {"$set": {f"dias-laborables.{yyyy_mm}": valor}}
        )
        return result.modified_count > 0

    def get_ultima_fecha_laborable_por_simbolo(self, simbolo: str):
        doc = self.collection.find_one({"simbolo": simbolo})
        if not doc or "dias-laborables" not in doc or not doc["dias-laborables"]:
            return None

        fechas = doc["dias-laborables"]
        ultima_fecha = max(fechas.keys())
        return {ultima_fecha: fechas[ultima_fecha]}

    def get_oficina_por_simbolo(self, simbolo: str):
        doc = self.collection.find_one({"simbolo": simbolo})
        return self._to_dict(doc) if doc else None
