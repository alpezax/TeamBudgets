from db.mongo_connection import getDb
from datetime import datetime

class Constantes:
    def __init__(self):
        self.collection = getDb()["constantes"]
        self.document = self._load_or_create()

    def _load_or_create(self):
        doc = self.collection.find_one({})
        if not doc:
            default = {
                "tiempo": {
                    "horas-jornada": 8
                },
                "tarifas": {
                    "2025-01": 48.5
                }
            }
            self.collection.insert_one(default)
            return default
        return doc

    def get_horas_jornada(self):
        return self.document.get("tiempo", {}).get("horas-jornada", 8)

    def set_horas_jornada(self, horas: int):
        self.collection.update_one({}, {"$set": {"tiempo.horas-jornada": horas}})
        self.document["tiempo"]["horas-jornada"] = horas

    def get_tarifa(self, yyyy_mm: str):
        return self.document.get("tarifas", {}).get(yyyy_mm)

    def set_tarifa(self, yyyy_mm: str, valor: float):
        self.collection.update_one({}, {"$set": {f"tarifas.{yyyy_mm}": valor}})
        self.document.setdefault("tarifas", {})[yyyy_mm] = valor

    def get_todas_tarifas(self):
        return self.document.get("tarifas", {})

    def get_ultima_tarifa(self):
        tarifas = self.document.get("tarifas", {})
        if not tarifas:
            return None
        fecha_mas_reciente = max(
            tarifas.keys(),
            key=lambda fecha: datetime.strptime(fecha, "%Y-%m")
        )
        return {fecha_mas_reciente: tarifas[fecha_mas_reciente]}

    def get_tarifa_mas_cercana(self, yyyy_mm: str):
        """
        Devuelve la tarifa más cercana anterior o igual a la fecha dada (YYYY-MM).
        """
        tarifas = self.document.get("tarifas", {})
        if not tarifas:
            return None

        target_date = datetime.strptime(yyyy_mm, "%Y-%m")
        fechas_validas = [
            fecha for fecha in tarifas
            if datetime.strptime(fecha, "%Y-%m") <= target_date
        ]
        if not fechas_validas:
            return None

        fecha_cercana = max(
            fechas_validas,
            key=lambda fecha: datetime.strptime(fecha, "%Y-%m")
        )
        return {fecha_cercana: tarifas[fecha_cercana]}
