from dotenv import load_dotenv
from utils import serviceCache

import os

load_dotenv()

def refresh_config():
    MONGO_URI = os.getenv("MONGO_URI")
    # Seleccionamos una base de datos en base a la cache
    entorno = serviceCache.get_data("ENTORNO")
    #print(f"Refrescando entorno: {entorno}")
    if entorno == 'PRO':
        DB_NAME = os.getenv("DB_NAME")
    elif entorno == 'PRE':
        DB_NAME = os.getenv("DB_NAME_PRE")
    elif entorno == 'TST1':
        DB_NAME = os.getenv("DB_NAME_TST1")
    elif entorno == 'TST2':
        DB_NAME = os.getenv("DB_NAME_TST2")
    elif entorno == 'TST3':
        DB_NAME = os.getenv("DB_NAME_TST3")
    else:
        print("Error. No hay base de datos seleccionada")
    return MONGO_URI,DB_NAME

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
refresh_config()