from db.mongo_connection import getDb
from bson import ObjectId
from utils import objectid_to_str

class CategoriaTrabajador:
    def __init__(self):
        self.collection = getDb()["categoria_trabajador"]

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

    def create(self, nombre: str, clase: str, simbolo: str, defaultcsr: float, csr: dict = None):
        new_doc = {
            "nombre": nombre,
            "clase": clase,
            "simbolo": simbolo,
            "defaultcsr": defaultcsr or 100, 
            "csr": csr or {}
        }
        result = self.collection.insert_one(new_doc)
        return str(result.inserted_id)

    def update(self, id_str: str, nombre: str = None, clase: str = None, simbolo: str = None):
        update_fields = {}
        if nombre is not None:
            update_fields["nombre"] = nombre
        if clase is not None:
            update_fields["clase"] = clase
        if simbolo is not None:
            update_fields["simbolo"] = simbolo

        result = self.collection.update_one(
            {"_id": ObjectId(id_str)},
            {"$set": update_fields}
        )
        return result.modified_count > 0

    def get_csr(self, id_str: str, yyyy_mm: str):
        doc = self.get_by_id(id_str)
        if doc and "csr" in doc:
            return doc["csr"].get(yyyy_mm)
        return None

    def set_csr(self, id_str: str, yyyy_mm: str, valor: int):
        result = self.collection.update_one(
            {"_id": ObjectId(id_str)},
            {"$set": {f"csr.{yyyy_mm}": valor}}
        )
        return result.modified_count > 0

    def delete(self, id_str: str):
        result = self.collection.delete_one({"_id": ObjectId(id_str)})
        return result.deleted_count > 0

    def get_ultimo_csr_por_simbolo(self, simbolo: str):
        doc = self.collection.find_one({"simbolo": simbolo})
        if not doc or "csr" not in doc or not doc["csr"]:
            return None

        csr_dict = doc["csr"]
        ultima_fecha = max(csr_dict.keys())
        return {ultima_fecha: csr_dict[ultima_fecha]}
    
    def get_categoria_por_simbolo(self, simbolo: str):
        """
        Devuelve el documento completo de una categoría dado su símbolo.
        """
        doc = self.collection.find_one({"simbolo": simbolo})
        if doc:
            return objectid_to_str.objectid_to_str(doc)
        return None