from db.mongo_connection import getDb

class ConstantesList:
    def __init__(self):
        self.collection = getDb()["constantes"]

    def get_all_constantes(self):
        """
        Devuelve una lista de todos los documentos en la colección 'constantes'.
        """
        return list(self.collection.find({}))
