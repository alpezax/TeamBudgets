import requests
from config import API_URL

#************************************************************************
# Funciones de la API para Trabajadores
#************************************************************************
def get_trabajadores():
    return requests.get(f"{API_URL}/trabajadores/").json()

def get_trabajador(id):
    return requests.get(f"{API_URL}/trabajador/{id}").json()

def crear_trabajador(nombre, oficina, categoria, alias, tags, workpool, dedicacion_mensual, coste_hora_mensual):
    data = {
        "nombre": nombre,
        "oficina": oficina,
        "categoria": categoria,
        "alias": alias,
        "tags": tags,
        "workpool": workpool,
        "dedicacion_mensual": dedicacion_mensual,
        "coste_hora_mensual": coste_hora_mensual
    }
    return requests.post(f"{API_URL}/trabajador/", json=data).json()

def actualizar_trabajador(id, data):
    return requests.put(f"{API_URL}/trabajador/{id}", json=data).json()

def eliminar_trabajador(id):
    return requests.delete(f"{API_URL}/trabajador/{id}").json()

def get_dedicacion_mensual(id, periodo):
    return requests.get(f"{API_URL}/trabajador/{id}/dedicacion/{periodo}").json()

def set_dedicacion_mensual(id, periodo, data):
    return requests.put(f"{API_URL}/trabajador/{id}/dedicacion/{periodo}", json=data).json()

def get_coste_hora_mensual(id, yyyy_mm):
    return requests.get(f"{API_URL}/trabajador/{id}/coste/{yyyy_mm}").json()

def set_coste_hora_mensual(id, yyyy_mm, valor):
    return requests.put(f"{API_URL}/trabajador/{id}/coste/{yyyy_mm}", json=valor).json()

#************************************************************************
# Funciones de la API para Categorías de Trabajador
#************************************************************************
def get_categorias():
    return requests.get(f"{API_URL}/categoria-trabajador/").json()

def get_categoria_by_id(id):
    return requests.get(f"{API_URL}/categoria-trabajador/{id}").json()

def get_categoria_by_simbolo(simbolo):
    return requests.get(f"{API_URL}/categoria-trabajador/simbolo/{simbolo}").json()

def get_ultimo_csr(simbolo):
    return requests.get(f"{API_URL}/categoria-trabajador/csr/{simbolo}/ultimo").json()

def get_csr_by_fecha(id, yyyy_mm):
    return requests.get(f"{API_URL}/categoria-trabajador/csr/{id}/{yyyy_mm}").json()

def crear_categoria(nombre, clase, simbolo):
    data = {"nombre": nombre, "clase": clase, "simbolo": simbolo}
    return requests.post(f"{API_URL}/categoria-trabajador/", json=data).json()

def actualizar_categoria(id, nombre=None, clase=None, simbolo=None):
    data = {"nombre": nombre, "clase": clase, "simbolo": simbolo}
    return requests.put(f"{API_URL}/categoria-trabajador/{id}", json=data).json()

def actualizar_csr(id, yyyy_mm, valor):
    data = {"valor": valor}
    return requests.put(f"{API_URL}/categoria-trabajador/csr/{id}/{yyyy_mm}", json=data).json()

def eliminar_categoria(id):
    return requests.delete(f"{API_URL}/categoria-trabajador/{id}").json()

#************************************************************************
# Funciones de la API para Oficinas
#************************************************************************
def get_oficinas():
    return requests.get(f"{API_URL}/oficina/").json()

def get_oficina(id):
    return requests.get(f"{API_URL}/oficina/{id}").json()

def crear_oficina(ciudad, tipo, simbolo):
    data = {"ciudad": ciudad, "tipo": tipo, "simbolo": simbolo}
    return requests.post(f"{API_URL}/oficina/", json=data).json()

def actualizar_oficina(id, ciudad, tipo, simbolo):
    data = {"ciudad": ciudad, "tipo": tipo, "simbolo": simbolo}
    return requests.put(f"{API_URL}/oficina/{id}", json=data).json()

def eliminar_oficina(id):
    return requests.delete(f"{API_URL}/oficina/{id}").json()

def set_dias_laborables(id, yyyy_mm, valor):
    return requests.put(f"{API_URL}/oficina/{id}/dias-laborables/{yyyy_mm}", params={"valor": valor}).json()

def get_dias_laborables(id, yyyy_mm):
    return requests.get(f"{API_URL}/oficina/{id}/dias-laborables/{yyyy_mm}").json()

def get_dias_laborables_all(id):
    return requests.get(f"{API_URL}/oficina/{id}/dias-laborables").json()

#************************************************************************
# Funciones de la API para Proyectos
#************************************************************************
def get_proyectos():
    return requests.get(f"{API_URL}/proyectos/").json()

def get_proyecto(id):
    return requests.get(f"{API_URL}/proyecto/{id}").json()

# Crear un proyecto con todos sus campos, incluyendo workpool y tarifa-hora
def crear_proyecto(nombre, idext, descripcion, horas, margen_contrato, workpool=None, tarifa_hora=None):
    data = {
        "nombre": nombre,
        "idext": idext,
        "descripcion": descripcion,
        "horas": horas,
        "margen_contrato": margen_contrato,
        "workpool": workpool or [],
        "tarifa_hora": tarifa_hora  # Añadido campo tarifa-hora
    }
    return requests.post(f"{API_URL}/proyecto/", json=data).json()

# Actualiza parcialmente un proyecto (nombre, horas, workpool, tarifa-hora, etc.)
def actualizar_proyecto(id, data):
    return requests.put(f"{API_URL}/proyecto/{id}", json=data).json()

def eliminar_proyecto(id):
    return requests.delete(f"{API_URL}/proyecto/{id}").json()

def get_horas_proyecto(id):
    return requests.get(f"{API_URL}/proyecto/{id}/horas").json()

def set_horas_proyecto(id, horas):
    return requests.put(f"{API_URL}/proyecto/{id}/horas", json=horas).json()

def get_margen_contrato(id, yyyy_mm):
    return requests.get(f"{API_URL}/proyecto/{id}/margen-contrato/{yyyy_mm}").json()

def set_margen_contrato(id, yyyy_mm, valor):
    return requests.put(f"{API_URL}/proyecto/{id}/margen-contrato/{yyyy_mm}", json=valor).json()

# Obtener la tarifa por hora de un proyecto
def get_tarifa_hora(id):
    return requests.get(f"{API_URL}/proyecto/{id}/tarifa-hora").json()

#************************************************************************
# Funciones de la API para Constantes
#************************************************************************
def get_constantes():
    return requests.get(f"{API_URL}/constantes").json()

def get_horas_jornada():
    return requests.get(f"{API_URL}/constantes/horas-jornada").json()['horas-jornada']

def set_horas_jornada(horas):
    data = {"horas": horas}
    return requests.post(f"{API_URL}/constantes/horas-jornada", json=data).json()

def set_tarifa(fecha, valor):
    data = {"fecha": fecha, "valor": valor}
    return requests.post(f"{API_URL}/constantes/tarifa", json=data).json()

def get_ultima_tarifa():
    d = requests.get(f"{API_URL}/constantes/ultima-tarifa").json()
    valor = next(iter(d.values()))
    return valor 

def get_tarifa_cercana(fecha):
    return requests.get(f"{API_URL}/constantes/tarifa-cercana/{fecha}").json()

#************************************************************************
# Funciones de la API para Documentos Genéricos
#************************************************************************

def get_document(collection_name, id=None):
    params = {"id": id} if id else {}
    return requests.get(f"{API_URL}/document/{collection_name}", params=params).json()

def get_field(collection_name, path, id=None):
    params = {"path": path}
    if id:
        params["id"] = id
    return requests.get(f"{API_URL}/document/{collection_name}/field", params=params).json()

def set_field(collection_name, path, value, id=None):
    data = {"path": path, "value": value}
    params = {"id": id} if id else {}
    return requests.post(f"{API_URL}/document/{collection_name}/field", json=data, params=params).json()

def update_fields(collection_name, updates, id=None):
    data = {"updates": updates}
    params = {"id": id} if id else {}
    return requests.put(f"{API_URL}/document/{collection_name}", json=data, params=params).json()

def delete_field(collection_name, path, id=None):
    data = {"path": path}
    params = {"id": id} if id else {}
    return requests.delete(f"{API_URL}/document/{collection_name}/field", json=data, params=params).json()

def delete_document(collection_name, id=None):
    params = {"id": id} if id else {}
    return requests.delete(f"{API_URL}/document/{collection_name}", params=params).json()

def create_document(collection_name, data=None):
    data = {"data": data or {}}
    return requests.post(f"{API_URL}/document/{collection_name}", json=data).json()

def get_documentos_de_coleccion(coleccion):
    """
    Recupera todos los documentos de una colección dada.
    """
    return requests.get(f"{API_URL}/document/{coleccion}").json()

def replace_entire_document(collection_name, new_data):
    """
    Reemplaza completamente un documento existente por uno nuevo.
    new_data debe incluir un campo "_id" válido (en string).
    """
    data = {"new_data": new_data}
    return requests.put(f"{API_URL}/document/{collection_name}/replace", json=data).json()

#************************************************************************
# Funciones de la API para Equipos
#************************************************************************

def get_equipos():
    return requests.get(f"{API_URL}/equipo/").json()

def get_equipo(id):
    return requests.get(f"{API_URL}/equipo/{id}").json()

def crear_equipo(nombre, descripcion, miembros=None, proyectos=None):
    data = {
        "nombre": nombre,
        "descripcion": descripcion,
        "miembros": miembros or [],
        "proyectos": proyectos or []
    }
    response = requests.post(f"{API_URL}/equipo/", json=data)
    try:
        return response.json()
    except:
        return {"error": response.text}

def actualizar_equipo(id, nombre=None, miembros=None, proyectos=None):
    data = {}
    if nombre is not None:
        data["nombre"] = nombre
    if miembros is not None:
        data["miembros"] = miembros
    if proyectos is not None:
        data["proyectos"] = proyectos
    response = requests.put(f"{API_URL}/equipo/{id}", json=data)
    try:
        return response.json()
    except:
        return {"error": response.text}

def eliminar_equipo(id):
    return requests.delete(f"{API_URL}/equipo/{id}").json()

def añadir_miembro_equipo(id_equipo, trabajador_id, participacion=100.0, nombre=""):
    """
    Añade un miembro a un equipo.
    """
    data = {
        "trabajador_id": trabajador_id,
        "participacion": participacion,
        "nombre": nombre
    }
    response = requests.post(f"{API_URL}/equipo/{id_equipo}/miembro/", json=data)
    try:
        return response.json()
    except:
        return {"error": response.text}

def actualizar_participacion_miembro(id_equipo, trabajador_id, nueva_participacion, nombre=""):
    data = {
        "trabajador_id": trabajador_id,
        "participacion": nueva_participacion,
        "nombre": nombre
    }
    response = requests.put(f"{API_URL}/equipo/{id_equipo}/miembro", json=data)
    try:
        return response.json()
    except:
        return {"error": response.text}

def vincular_proyecto_equipo(id_equipo, id_proyecto):
    """
    Vincula un proyecto a un equipo.
    """
    response = requests.post(f"{API_URL}/equipo/{id_equipo}/vincular_proyecto/{id_proyecto}")
    try:
        return response.json()
    except:
        return {"error": response.text}

def desvincular_proyecto_equipo(id_equipo, id_proyecto):
    """
    Desvincula un proyecto de un equipo.
    """
    response = requests.delete(f"{API_URL}/equipo/{id_equipo}/desvincular_proyecto/{id_proyecto}")
    try:
        return response.json()
    except:
        return {"error": response.text}

#************************************************************************
# Funciones de la API para Validación de Presupuestos
#************************************************************************
def validar_presupuesto(presupuesto_id):
    """Valida un presupuesto sin hacer update en la base de datos."""
    data = {"presupuesto_id": presupuesto_id}
    response = requests.post(f"{API_URL}/presupuestos/validar", json=data)
    try:
        return response.json()
    except:
        return {"error": response.text}

def validar_y_actualizar_presupuesto(presupuesto_id):
    """Valida y actualiza el estado del presupuesto en la base de datos."""
    data = {"presupuesto_id": presupuesto_id}
    response = requests.post(f"{API_URL}/presupuestos/validarupdate", json=data)
    try:
        return response.json()
    except:
        return {"error": response.text}
    

def aplicar_presupuesto(presupuesto_id):
    """Lanza la aplicación del presupuesto con ID dado."""
    url = f"{API_URL}/presupuestos/{presupuesto_id}/aplicar"
    response = requests.post(url)
    try:
        return response.json()
    except:
        return {"error": response.text}