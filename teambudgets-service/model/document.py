from db.mongo_connection import getDb
from bson.objectid import ObjectId
from typing import Optional, Dict, Any
from bson import ObjectId
from utils.objectid_to_str import objectid_to_str

class Document:
    def __init__(self, collection_name: str, document_filter: Optional[Dict[str, Any]] = None):
        """
        :param collection_name: Nombre de la colección en MongoDB.
        :param document_filter: Filtro para buscar el documento. Si no se proporciona, se usará {} (primer documento).
        """
        self.collection = getDb()[collection_name]
        self.document_filter = document_filter or {}
        self.document = self._load_or_create()

    def _load_or_create(self) -> Dict:
        doc = self.collection.find_one(self.document_filter)
        if not doc:
            self.collection.insert_one({})
            return self.collection.find_one(self.document_filter)
        return doc

    def get(self, path: str, default=None):
        """
        Obtiene un valor anidado en el documento con notación punto.
        """
        keys = path.split(".")
        current = self.document
        for key in keys:
            current = current.get(key, default)
            if current == default:
                break
        return current

    def set(self, path: str, value: Any):
        """
        Establece un valor anidado en el documento con notación punto.
        """
        self.collection.update_one(self.document_filter, {"$set": {path: value}})
        keys = path.split(".")
        d = self.document
        for key in keys[:-1]:
            d = d.setdefault(key, {})
        d[keys[-1]] = value

    def update(self, updates: Dict[str, Any]):
        """
        Actualiza múltiples campos del documento.
        """
        self.collection.update_one(self.document_filter, {"$set": updates['data']})
        for path, value in updates.items():
            self.set(path, value)

    def update_total(self, new_data: Dict[str, Any]):
        """
        Reemplaza todo el contenido del documento con nuevos datos.
        Utiliza el _id para encontrar el documento a actualizar.
        """
        if '_id' not in new_data:
            raise ValueError("El documento debe contener el campo '_id' para ser actualizado.")
        
        # Reemplaza el documento completo
        self.collection.replace_one({'_id': ObjectId(new_data['_id'])}, new_data)
        self.document = new_data  # Actualiza el documento en la memoria
    
    def delete_field(self, path: str):
        """
        Elimina un campo anidado del documento con notación punto.
        """
        self.collection.update_one(self.document_filter, {"$unset": {path: ""}})
        # No se elimina del cache `self.document`, se podría recargar si fuera necesario

    def delete_document(self):
        """
        Elimina completamente el documento de la colección.
        """
        self.collection.delete_one(self.document_filter)
        self.document = {}

    def reload(self):
        """
        Recarga el documento desde la base de datos.
        """
        self.document = self.collection.find_one(self.document_filter)

    def get_document(self) -> Dict:
        """
        Devuelve el documento completo.
        """
        return self.document

    def get_id(self) -> Optional[str]:
        return str(self.document.get("_id")) if self.document else None

    def create(self, data: dict) -> ObjectId:
        result = objectid_to_str(self.collection.insert_one(data))
        return result.inserted_id

    def get_all_documents(self, collection_name: str) -> list[dict]:
        collection = getDb()[collection_name]
        cursor = collection.find()
        documents = list(cursor)
        return [objectid_to_str(doc) for doc in documents]
    
    def set_or_create_field(self, path: str, value: Any):
        """
        Establece el valor de un campo. Si el campo existe, lo actualiza; si no, lo crea.
        El campo se especifica usando notación punto para estructuras anidadas.
        """
        self.collection.update_one(self.document_filter, {"$set": {path: value}})
        
        # También actualiza la copia en memoria
        keys = path.split(".")
        d = self.document
        for key in keys[:-1]:
            d = d.setdefault(key, {})
        d[keys[-1]] = value