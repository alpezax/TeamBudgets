from db.mongo_connection import getDb
from bson import ObjectId
from utils.objectid_to_str import objectid_to_str
from typing import List, Optional


class Equipo:
    def __init__(self):
        self.collection = getDb()["equipo"]

    def _to_dict(self, doc):
        if doc:
            doc["_id"] = str(doc["_id"])
            if "miembros" in doc:
                for miembro in doc["miembros"]:
                    miembro["trabajador_id"] = str(miembro["trabajador_id"])
        return doc

    def get_all(self):
        return [self._to_dict(doc) for doc in self.collection.find()]

    def get_by_id(self, id_str: str):
        try:
            doc = self.collection.find_one({"_id": ObjectId(id_str)})
            return self._to_dict(doc)
        except Exception:
            return None

    def create(self, nombre: str, miembros: Optional[List[dict]] = None, descripcion: Optional[str] = ""):
        """
        Crea un nuevo equipo.
        :param nombre: Nombre del equipo.
        :param miembros: Lista de diccionarios con claves: trabajador_id (str) y participacion (float). Opcional.
        :param descripcion: Texto descriptivo del equipo. Opcional.
        """
        miembros_normalizados = []
        if miembros:
            for m in miembros:
                miembros_normalizados.append({
                    "trabajador_id": ObjectId(m["trabajador_id"]),
                    "participacion": m.get("participacion", 100.0)
                })

        new_doc = {
            "nombre": nombre,
            "descripcion": descripcion,
            "miembros": miembros_normalizados or []
        }

        result = self.collection.insert_one(new_doc)
        return objectid_to_str(result.inserted_id)

    def update(self, id_str: str, nombre: str = None, miembros: list = None):
        update_fields = {}
        if nombre is not None:
            update_fields["nombre"] = nombre
        if miembros is not None:
            miembros_normalizados = [
                {
                    "trabajador_id": ObjectId(m["trabajador_id"]),
                    "participacion": m.get("participacion", 100.0)
                } for m in miembros
            ]
            update_fields["miembros"] = miembros_normalizados

        result = self.collection.update_one(
            {"_id": ObjectId(id_str)},
            {"$set": update_fields}
        )
        return result.modified_count > 0

    def delete(self, id_str: str):
        result = self.collection.delete_one({"_id": ObjectId(id_str)})
        return result.deleted_count > 0

    def add_miembro(self, equipo_id: str, trabajador_id: str, nombre: str, participacion: float = 100.0):
        """
        Agrega un miembro a un equipo.
        :param equipo_id: ID del equipo donde se añadirá el miembro.
        :param trabajador_id: ID del trabajador.
        :param participacion: Porcentaje de participación del miembro.
        """
        result = self.collection.update_one(
            {"_id": ObjectId(equipo_id)},  # Encontramos el equipo por su ID
            {"$push": {
                "miembros": {
                    "trabajador_id": ObjectId(trabajador_id),
                    "participacion": participacion,
                    "nombre": nombre
                }
            }}
        )
        return result.modified_count > 0  # Retorna True si se modificó el equipo, False si no

    def remove_miembro(self, equipo_id: str, trabajador_id: str):
        result = self.collection.update_one(
            {"_id": ObjectId(equipo_id)},
            {"$pull": {
                "miembros": {
                    "trabajador_id": ObjectId(trabajador_id)
                }
            }}
        )
        return result.modified_count > 0

    def actualizar_participacion_miembro(self, equipo_id: str, trabajador_id: str, participacion: float):
        result = self.collection.update_one(
            {
                "_id": ObjectId(equipo_id),
                "miembros.trabajador_id": ObjectId(trabajador_id)
            },
            {
                "$set": {
                    "miembros.$.participacion": participacion
                }
            }
        )
        return result.modified_count > 0