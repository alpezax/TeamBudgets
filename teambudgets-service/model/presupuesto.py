from db.mongo_connection import getDb
from bson import ObjectId
from utils import objectid_to_str
from datetime import datetime

class Presupuesto:
    def __init__(self):
        self.collection = getDb()["presupuestos"]

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

    def create(self, nombre_balance: str, mes: str, año: int, version="1.0.0", estado="DRAFT", imputaciones=None):
        mes_anyo_str = f"{año}-{str(datetime.strptime(mes, '%B').month).zfill(2)}"
        mes_anyo_timestamp = f"{mes_anyo_str}-01T00:00:00"
        now_timestamp = datetime.utcnow().isoformat()

        new_doc = {
            "nombre_balance": nombre_balance,
            "estado": estado,
            "version": version,
            "mes": mes,
            "año": año,
            "mes_anyo_str": mes_anyo_str,
            "mes_anyo_timestamp": mes_anyo_timestamp,
            "history": {},
            "equipo": {},
            "imputaciones": imputaciones or [],
            "total_balance": 0,
            "timestamp": now_timestamp
        }

        result = self.collection.insert_one(new_doc)
        return str(result.inserted_id)

    def update_estado(self, id_str: str, nuevo_estado: str):
        result = self.collection.update_one(
            {"_id": ObjectId(id_str)},
            {"$set": {"estado": nuevo_estado}}
        )
        return result.modified_count > 0

    def add_imputacion(self, id_str: str, imputacion: dict):
        result = self.collection.update_one(
            {"_id": ObjectId(id_str)},
            {"$push": {"imputaciones": imputacion}}
        )
        return result.modified_count > 0

    def update_total_balance(self, id_str: str, nuevo_balance: float):
        result = self.collection.update_one(
            {"_id": ObjectId(id_str)},
            {"$set": {"total_balance": nuevo_balance}}
        )
        return result.modified_count > 0

    def delete(self, id_str: str):
        result = self.collection.delete_one({"_id": ObjectId(id_str)})
        return result.deleted_count > 0
