from fastapi import FastAPI
from controller import constantesController
from controller import categoriaTrabajadorController
from controller import oficinaController
from controller import proyectoController
from controller import trabajadorController
from controller import datacacheController
from controller import taskController
from controller import documentController
from controller import equipoController
from controller import costesEquipoServiceController
from controller import autoBalanceServiceController
from controller import autoBalanceReportController

app = FastAPI()
app.include_router(constantesController.router)
app.include_router(categoriaTrabajadorController.router)
app.include_router(oficinaController.router)
app.include_router(proyectoController.router)
app.include_router(trabajadorController.router)
app.include_router(datacacheController.router)
app.include_router(taskController.router)
app.include_router(documentController.router)
app.include_router(equipoController.router)
app.include_router(autoBalanceServiceController.router)
app.include_router(costesEquipoServiceController.router)
app.include_router(autoBalanceReportController.router)

