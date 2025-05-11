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
            if "proyectos" in doc:
                doc["proyectos"] = [str(pid) for pid in doc["proyectos"]]
        return doc

    def get_all(self):
        return [self._to_dict(doc) for doc in self.collection.find()]

    def get_by_id(self, id_str: str):
        try:
            doc = self.collection.find_one({"_id": ObjectId(id_str)})
            return self._to_dict(doc)
        except Exception:
            return None

    def create(self, nombre: str, miembros: Optional[List[dict]] = None,
               descripcion: Optional[str] = "", proyectos: Optional[List[str]] = None):
        miembros_normalizados = []
        if miembros:
            for m in miembros:
                miembros_normalizados.append({
                    "trabajador_id": ObjectId(m["trabajador_id"]),
                    "participacion": m.get("participacion", 100.0)
                })

        proyectos_obj = [ObjectId(p) for p in proyectos] if proyectos else []

        new_doc = {
            "nombre": nombre,
            "descripcion": descripcion,
            "miembros": miembros_normalizados,
            "proyectos": proyectos_obj
        }

        result = self.collection.insert_one(new_doc)
        return objectid_to_str(result.inserted_id)

    def update(self, id_str: str, nombre: str = None, miembros: list = None, proyectos: List[str] = None):
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
        if proyectos is not None:
            update_fields["proyectos"] = [ObjectId(p) for p in proyectos]

        result = self.collection.update_one(
            {"_id": ObjectId(id_str)},
            {"$set": update_fields}
        )
        return result.modified_count > 0

    def delete(self, id_str: str):
        result = self.collection.delete_one({"_id": ObjectId(id_str)})
        return result.deleted_count > 0

    def add_miembro(self, equipo_id: str, trabajador_id: str, nombre: str, participacion: float = 100.0):
        result = self.collection.update_one(
            {"_id": ObjectId(equipo_id)},
            {"$push": {
                "miembros": {
                    "trabajador_id": ObjectId(trabajador_id),
                    "participacion": participacion,
                    "nombre": nombre
                }
            }}
        )
        return result.modified_count > 0

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

    def vincular_proyecto(self, equipo_id: str, proyecto_id: str):
        result = self.collection.update_one(
            {"_id": ObjectId(equipo_id)},
            {"$addToSet": {"proyectos": ObjectId(proyecto_id)}}
        )
        return result.modified_count > 0

    def desvincular_proyecto(self, equipo_id: str, proyecto_id: str):
        result = self.collection.update_one(
            {"_id": ObjectId(equipo_id)},
            {"$pull": {"proyectos": ObjectId(proyecto_id)}}
        )
        return result.modified_count > 0
