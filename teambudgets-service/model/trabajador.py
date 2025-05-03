from db.mongo_connection import getDb
from bson import ObjectId
from utils.objectid_to_str import objectid_to_str

class Trabajador:
    def __init__(self):
        self.collection = getDb()["trabajador"]

    def _to_dict(self, doc):
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc


    def get_all(self):
        trabajadores = list(self.collection.find())
        return [objectid_to_str(doc) for doc in trabajadores]

    def get_by_id(self, id_str: str):
        try:
            doc = self.collection.find_one({"_id": ObjectId(id_str)})
            return self._to_dict(doc)
        except Exception:
            return None

    def create(self, nombre: str, oficina: str, categoria: str, alias: str, tags: list = None,
               workpool: list = None, dedicacion_mensual: dict = None, coste_hora_mensual: dict = None):
        new_doc = {
            "nombre": nombre,
            "oficina": ObjectId(oficina),
            "categoria": ObjectId(categoria),
            "alias": alias,
            "tags": tags or [],
            "workpool": workpool or [],
            "dedicacion-mensual": dedicacion_mensual or {},
            "coste-hora-mensual": coste_hora_mensual or {}
        }
        result = self.collection.insert_one(new_doc)
        return str(result.inserted_id)

    def update(self, id_str: str, **kwargs):
        update_fields = {}
        for field, value in kwargs.items():
            if field in ["oficina", "categoria"] and value:
                update_fields[field] = ObjectId(value)
            elif value is not None:
                update_fields[field] = value

        result = self.collection.update_one(
            {"_id": ObjectId(id_str)},
            {"$set": update_fields}
        )
        return result.modified_count > 0

    def delete(self, id_str: str):
        result = self.collection.delete_one({"_id": ObjectId(id_str)})
        return result.deleted_count > 0

    def get_dedicacion_mensual(self, id_str: str, periodo: str):
        doc = self.get_by_id(id_str)
        if doc:
            return doc.get("dedicacion-mensual", {}).get(periodo)
        return None

    def set_dedicacion_mensual(self, id_str: str, periodo: str, data: dict):
        result = self.collection.update_one(
            {"_id": ObjectId(id_str)},
            {"$set": {f"dedicacion-mensual.{periodo}": data}}
        )
        return result.modified_count > 0

    def get_coste_hora_mensual(self, id_str: str, yyyy_mm: str):
        doc = self.get_by_id(id_str)
        if doc:
            return doc.get("coste-hora-mensual", {}).get(yyyy_mm)
        return None

    def set_coste_hora_mensual(self, id_str: str, yyyy_mm: str, valor: float):
        result = self.collection.update_one(
            {"_id": ObjectId(id_str)},
            {"$set": {f"coste-hora-mensual.{yyyy_mm}": valor}}
        )
        return result.modified_count > 0
    
    def get_dedicaciones_por_mes(self, yyyy_mm: str):
        """
        Devuelve un diccionario con el ID del trabajador como clave y la dedicación mensual como valor,
        solo para el mes especificado.
        """
        resultados = {}
        for doc in self.collection.find({f"dedicacion-mensual.{yyyy_mm}": {"$exists": True}}):
            dedicacion = doc.get("dedicacion-mensual", {}).get(yyyy_mm)
            if dedicacion:
                resultados[str(doc["_id"])] = dedicacion
        return resultados

    def get_costes_por_mes(self, yyyy_mm: str):
        """
        Devuelve un diccionario con el ID del trabajador como clave y el coste-hora mensual como valor,
        solo para el mes especificado.
        """
        resultados = {}
        for doc in self.collection.find({f"coste-hora-mensual.{yyyy_mm}": {"$exists": True}}):
            coste = doc.get("coste-hora-mensual", {}).get(yyyy_mm)
            if coste is not None:
                resultados[str(doc["_id"])] = coste
        return resultados

    def get_by_alias(self, alias: str):
        """
        Devuelve un trabajador por su alias.
        """
        doc = self.collection.find_one({"alias": alias})
        if doc:
            return objectid_to_str(doc)
        return None
    
    def get_ultimo_coste_hora(self, id_str: str):
        """
        Retorna el último coste-hora mensual registrado para un trabajador, basado en la clave más reciente (yyyy-mm).
        """
        doc = self.get_by_id(id_str)
        if not doc:
            return None
        
        costes = doc.get("coste-hora-mensual", {})
        if not costes:
            return None

        # Ordenar las claves yyyy-mm y obtener la más reciente
        fechas_ordenadas = sorted(costes.keys(), reverse=True)
        fecha_mas_reciente = fechas_ordenadas[0]
        return {
            "periodo": fecha_mas_reciente,
            "coste_hora": costes[fecha_mas_reciente]
        }    