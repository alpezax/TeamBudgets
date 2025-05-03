import json
import os

FILENAME = "service-cache.json"

def load_data():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=4)

def set_data(key: str, value):
    data = load_data()
    data[key] = value  
    save_data(data)
    #print(f"[SET] {key} = {value}")

def set_data_bulk(new_data: dict):
    data = load_data()
    data.update(new_data)
    save_data(data)
    #print(f"[SET BULK] {str(new_data)}")

def get_data(key: str):
    data = load_data()
    value = data.get(key)
    #print(f"[GET] {key} = {value}")
    return value

