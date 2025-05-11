from db.mongo_connection import getDb
from bson import ObjectId
import uuid
import datetime

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
        
    def create(self, nombre: str, idext: str, descripcion: str, horas: dict = None, margen_contrato: dict = None, tarifa_hora: float = None):
        new_doc = {
            "nombre": nombre,
            "idext": idext,
            "descripcion": descripcion,
            "horas": horas or {"venta": 0, "consumidas": 0},
            "margen-contrato": margen_contrato or {},
            "workpool": [],
            "tarifa-hora": tarifa_hora 
        }
        result = self.collection.insert_one(new_doc)
        return str(result.inserted_id)
    
    def update(self, id_str: str, nombre: str = None, idext: str = None, descripcion: str = None,
            horas: dict = None, workpool: list = None, tarifa_hora: float = None):
        update_fields = {}
        if nombre is not None:
            update_fields["nombre"] = nombre
        if idext is not None:
            update_fields["idext"] = idext
        if descripcion is not None:
            update_fields["descripcion"] = descripcion
        if horas is not None:
            update_fields["horas"] = horas
        if workpool is not None:
            update_fields["workpool"] = workpool
        if tarifa_hora is not None:
            update_fields["tarifa-hora"] = tarifa_hora 
        if not update_fields:
            return False

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

    def aplica_transaccion(self, id_proyecto: str, horas: float, presupuesto_id: str, presupuesto_nombre: str, mes_str: str, txid: str):
        try:
            proyecto = self.collection.find_one({"_id": ObjectId(id_proyecto)})
            if not proyecto:
                return False

            # Sumar horas a las consumidas
            horas_actuales = proyecto.get("horas", {"venta": 0, "consumidas": 0})
            horas_actuales["consumidas"] = horas_actuales.get("consumidas", 0) + horas

            # Nueva transacción
            nueva_tx = {
                "mes_str": mes_str,
                "txid": txid, #str(uuid.uuid4()),
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "horas": horas,
                "presupuesto-id": presupuesto_id,
                "presupuesto-name": presupuesto_nombre
            }

            # Si no existe 'tx', lo inicializamos como lista vacía
            txs = proyecto.get("tx", [])
            txs.append(nueva_tx)

            # Actualizamos el documento
            result = self.collection.update_one(
                {"_id": ObjectId(id_proyecto)},
                {"$set": {"horas": horas_actuales, "tx": txs}}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error al aplicar transacción: {e}")
            return False

    def rollback_transaccion(self, id_proyecto: str, txid: str):
        try:
            proyecto = self.collection.find_one({"_id": ObjectId(id_proyecto)})
            if not proyecto or "tx" not in proyecto:
                return False

            txs = proyecto["tx"]
            tx_to_rollback = next((tx for tx in txs if tx["txid"] == txid), None)

            if not tx_to_rollback:
                return False  # No se encontró la transacción

            horas_a_restar = tx_to_rollback["horas"]
            nuevas_txs = [tx for tx in txs if tx["txid"] != txid]

            horas_actuales = proyecto.get("horas", {"venta": 0, "consumidas": 0})
            horas_actuales["consumidas"] = max(0, horas_actuales.get("consumidas", 0) - horas_a_restar)

            result = self.collection.update_one(
                {"_id": ObjectId(id_proyecto)},
                {"$set": {"horas": horas_actuales, "tx": nuevas_txs}}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error al hacer rollback de la transacción: {e}")
            return False
