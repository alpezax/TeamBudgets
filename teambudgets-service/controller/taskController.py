from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import importlib
import os
import traceback

router = APIRouter()

class TaskRequest(BaseModel):
    task_name: str

@router.post("/task/execute")
def execute_task(request: TaskRequest):
    try:
        task_module_name = request.task_name
        print(f"Intentando importar: tasks.{task_module_name}")

        # Import dinámico del módulo
        module = importlib.import_module(f"tasks.{task_module_name}")
        
        # Ejecutar la función principal del script (esperamos que tenga `run()`)
        if hasattr(module, "run") and callable(module.run):
            module.run()
            return {"status": "success", "message": f"Tarea '{task_module_name}' ejecutada correctamente."}
        else:
            raise HTTPException(status_code=400, detail=f"La tarea '{task_module_name}' no tiene una función 'run()' ejecutable.")

    except ModuleNotFoundError:
        print(f"ModuleNotFoundError: tasks.{request.task_name}")
        traceback.print_exc()
        raise HTTPException(status_code=404, detail=f"No se encontró la tarea '{request.task_name}' en el módulo 'tasks'.")
    except Exception as e:
        traceback_str = traceback.format_exc()
        print(f"Error ejecutando la tarea '{request.task_name}':\n{traceback_str}")
        raise HTTPException(status_code=500, detail=f"Error al ejecutar la tarea: {str(e)}\n{traceback_str}")

@router.get("/task/list", response_model=List[str])
def list_tasks():
    tasks_dir = os.path.join(os.path.dirname(__file__), "../tasks")
    files = [
        f[:-3]
        for f in os.listdir(tasks_dir)
        if f.endswith(".py") and f != "__init__.py"
    ]
    return sorted(files)