from pymongo import MongoClient
from .config import MONGO_URI, DB_NAME, refresh_config

def getDb():
    MONGO_URI,DB_NAME = refresh_config()
    print(f"Get db: {DB_NAME}")
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db