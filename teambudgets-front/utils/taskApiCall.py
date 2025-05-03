import requests
from config import API_URL

def get_tasks():
    response = requests.get(f"{API_URL}/task/list")
    return response.json()

def ejecutar_task(task_name):
    response = requests.post(f"{API_URL}/task/execute", json={"task_name": task_name})
    return response.json()