from datetime import datetime
from typing import List, Dict
from bson import ObjectId
from abc import ABC, abstractmethod

from model.trabajador import Trabajador
from model.equipo import Equipo
from model.proyecto import Proyecto
from model.oficina import Oficina
from utils.objectid_to_str import objectid_to_str
from dateutil.relativedelta import relativedelta

# --- Interfaz común para reglas de validación ---
class ValidationRule(ABC):
    @abstractmethod
    def validate(self, document: Dict) -> Dict:
        """Retorna un dict con status: OK | WARN | KO y mensajes de error si los hay."""
        pass

# --- Validación 1: Todos los miembros han imputado todas las horas ---
class FullHoursImputedValidation(ValidationRule):
    def validate(self, document: Dict) -> Dict:
        errores: List[str] = []
        ok_messages: List[str] = []
        equipo_id = document['equipo']['id']
        periodo = document.get("mes_anyo_str") 
        trabajadores_horas: Dict[str, float] = {}

        # Recuperar todos los miembros del equipo
        equipo = Equipo().get_by_id(equipo_id)
        if not equipo:
            errores.append(f"Equipo con ID {equipo_id} no encontrado.")
            return {"status": "KO", "errors": errores, "ok_messages": []}

        miembros = equipo.get("miembros", [])
        dedicaciones = Trabajador().get_dedicaciones_por_mes(periodo)
        
        for miembro in miembros:
            trabajador_id = str(miembro["trabajador_id"])
            participacion = miembro["participacion"] / 100
            dedicacion = dedicaciones.get(trabajador_id)
            trabajador = Trabajador().get_by_id(trabajador_id)
            nombre = trabajador.get("nombre", f"Trabajador {trabajador_id}")

            if not dedicacion:
                errores.append(f"{nombre} no ha imputado horas para el mes {periodo}.")
            else:
                horas_esperadas = (dedicacion.get('laborables') - dedicacion.get('vacaciones')) * 8 * participacion
                horas_imputadas = sum(
                    gasto["horas"] for imputacion in document.get("imputaciones", [])
                    for gasto in imputacion.get("gastos", []) if gasto["trabajador_id"] == trabajador_id
                )

                if horas_imputadas != horas_esperadas:
                    errores.append(f"{nombre} ha imputado {horas_imputadas}h, se esperaban {horas_esperadas}h.")
                else:
                    ok_messages.append(f"{nombre} ha imputado correctamente {horas_imputadas}h en el mes {periodo}.")

        status = "OK" if not errores else "KO"
        return {"status": status, "errors": errores, "ok_messages": ok_messages}

# --- Servicio para consultar horas restantes de proyecto ---
class ProyectoService:
    def __init__(self, proyectos_collection = None):
        self.proyecto_model = Proyecto()  # Utilizamos la clase Proyecto

    def get_remaining_hours(self, proyecto_id: str) -> float:
        proyecto = self.proyecto_model.get_by_id(proyecto_id)
        if proyecto and "horas" in proyecto:
            horas_venta = proyecto["horas"].get("venta", 0)
            horas_consumidas = proyecto["horas"].get("consumidas", 0)
            return horas_venta - horas_consumidas
        return 0.0

# --- Validación 2: A todos los proyectos les quedan horas disponibles ---
class ProjectsHaveAvailableHoursValidation(ValidationRule):
    def __init__(self, proyectos_service: ProyectoService):
        self.proyectos_service = proyectos_service

    def validate(self, document: Dict) -> Dict:
        errores: List[str] = []
        ok_messages: List[str] = []

        imputaciones = document.get("imputaciones", [])
        for imputacion in imputaciones:
            pid = imputacion.get("proyecto_id")
            horas_imputadas = imputacion.get("horas", 0)
            horas_disponibles = self.proyectos_service.get_remaining_hours(pid)
            proyecto = Proyecto().get_by_id(pid)
            nombre = proyecto.get("nombre", f"Proyecto {pid}")

            if horas_disponibles < horas_imputadas:
                errores.append(
                    f"{nombre} no tiene suficientes horas disponibles: {horas_disponibles}h disponibles, {horas_imputadas}h imputadas."
                )
            else:
                ok_messages.append(
                    f"{nombre} tiene suficientes horas disponibles: {horas_disponibles}h disponibles, {horas_imputadas}h imputadas."
                )

        status = "OK" if not errores else "KO"
        return {"status": status, "errors": errores, "ok_messages": ok_messages}

# --- Servicio principal que aplica todas las validaciones ---
class BudgetValidationService:
    def __init__(self, presupuestos_collection, validation_rules: List[ValidationRule]):
        self.presupuestos_collection = presupuestos_collection
        self.validation_rules = validation_rules

    def validate_presupuesto(self, presupuesto_id: str) -> Dict:
        document = self.presupuestos_collection.find_one({"_id": ObjectId(presupuesto_id)})
        if not document:
            return {
                "status": "KO",
                "errors": [f"Presupuesto con id {presupuesto_id} no encontrado."],
                "validations_ok": []
            }

        resultados: List[Dict] = []
        final_status = "OK"
        all_errors: List[str] = []
        all_ok_messages: List[str] = []

        for rule in self.validation_rules:
            resultado = rule.validate(document)
            resultados.append(resultado)

            if resultado["status"] == "KO":
                final_status = "KO"
            elif resultado["status"] == "WARN" and final_status != "KO":
                final_status = "WARN"

            all_errors.extend(resultado.get("errors", []))
            all_ok_messages.extend(resultado.get("ok_messages", []))

        return {
            "status": final_status,
            "errors": all_errors,
            "validations_ok": all_ok_messages,
            "full_result": resultados
        }

    def validate_and_update(self, presupuesto_id: str) -> Dict:
        validation_result = self.validate_presupuesto(presupuesto_id)

        estado = "VALID" if validation_result["status"] == "OK" else "INVALID"

        update_result = self.presupuestos_collection.update_one(
            {"_id": ObjectId(presupuesto_id)},
            {
                "$set": {
                    "estado": estado,
                    "validations": validation_result["full_result"]
                }
            }
        )

        return {
            "update_status": "OK" if update_result.modified_count == 1 else "NO_CHANGE",
            "estado": estado,
            "validations": validation_result["full_result"],
            "errors": validation_result.get("errors", []),
            "validations_ok": validation_result.get("validations_ok", [])
        }
