import streamlit as st
from components.sidebar import sidebar_config 
from utils.objectApiCall import *
from components.auth import authenticate

# Título de la aplicación
st.title("Gestión de Proyectos")
# Autenticación
if not authenticate():
    st.stop()
    
sidebar_config()
# Mostrar todos los proyectos
st.header("📋 Proyectos registrados")
proyectos = get_proyectos()
for proyecto in proyectos:
    with st.expander(f"{proyecto['nombre']} (ID Externo: {proyecto['idext']})"):
        st.json(proyecto)

# Crear nuevo proyecto
st.header("➕ Crear Proyecto")
with st.form("crear_proyecto"):
    nombre = st.text_input("Nombre del Proyecto")
    idext = st.text_input("ID Externo")
    descripcion = st.text_area("Descripción")
    horas = {
        "venta": st.number_input("Horas de venta", min_value=0, value=0),
        "consumidas": st.number_input("Horas consumidas", min_value=0, value=0)
    }
    margen_contrato = {
        "margen": st.number_input("Margen de contrato", min_value=0.0, format="%.2f")
    }
    tarifa_hora = st.number_input("Tarifa por hora", min_value=0.0, format="%.2f")  # Campo de tarifa por hora
    workpool_input = st.text_area("Workpool (separado por comas)", "")
    workpool = [w.strip() for w in workpool_input.split(",")] if workpool_input else []
    submitted = st.form_submit_button("Crear Proyecto")
    if submitted:
        res = crear_proyecto(nombre, idext, descripcion, horas, margen_contrato, workpool, tarifa_hora)  # Añadido tarifa_hora
        st.success(f"Proyecto creado: {res}")

# Actualizar proyecto
st.header("✏️ Actualizar Proyecto")
id_update = st.text_input("ID de proyecto a actualizar")
if id_update:
    proyecto = get_proyecto(id_update)
    if proyecto:
        nombre_u = st.text_input("Nombre", proyecto.get("nombre"))
        idext_u = st.text_input("ID Externo", proyecto.get("idext"))
        descripcion_u = st.text_area("Descripción", proyecto.get("descripcion"))
        horas_u = proyecto.get("horas", {})
        horas = {
            "venta": st.number_input("Horas de venta", min_value=0, value=horas_u.get("venta", 0)),
            "consumidas": st.number_input("Horas consumidas", min_value=0, value=horas_u.get("consumidas", 0))
        }
        margen_contrato_u = proyecto.get("margen_contrato", {})
        margen = {
            "margen": st.number_input("Margen de contrato", min_value=0.0, value=margen_contrato_u.get("margen", 0.0), format="%.2f")
        }
        tarifa_hora_u = proyecto.get("tarifa_hora", 0.0)  # Mostrar tarifa por hora
        tarifa_hora = st.number_input("Tarifa por hora", min_value=0.0, value=tarifa_hora_u, format="%.2f")
        workpool_u = proyecto.get("workpool", [])
        workpool_input = st.text_area("Workpool (separado por comas)", ", ".join(workpool_u))
        workpool = [w.strip() for w in workpool_input.split(",")] if workpool_input else []
        if st.button("Actualizar"):
            data = {
                "nombre": nombre_u,
                "idext": idext_u,
                "descripcion": descripcion_u,
                "horas": horas,
                "margen_contrato": margen,
                "workpool": workpool,
                "tarifa_hora": tarifa_hora  # Incluir tarifa-hora en la actualización
            }
            res = actualizar_proyecto(id_update, data)
            st.success("Proyecto actualizado correctamente" if res else "No se pudo actualizar el proyecto")

# Eliminar proyecto
st.header("🗑️ Eliminar Proyecto")
id_delete = st.text_input("ID de proyecto a eliminar")
if st.button("Eliminar"):
    res = eliminar_proyecto(id_delete)
    st.warning("Proyecto eliminado correctamente" if res else "No se pudo eliminar el proyecto")

# Gestionar horas de proyecto
st.header("⏱️ Gestión de Horas del Proyecto")
id_horas = st.text_input("ID de proyecto para horas")
if id_horas:
    horas_proyecto = get_horas_proyecto(id_horas)
    if horas_proyecto:
        st.write(horas_proyecto)
    nueva_venta = st.number_input("Nuevo valor de horas de venta", min_value=0, value=0)
    nuevas_consumidas = st.number_input("Nuevo valor de horas consumidas", min_value=0, value=0)
    if st.button("Actualizar horas del proyecto"):
        res = set_horas_proyecto(id_horas, {"venta": nueva_venta, "consumidas": nuevas_consumidas})
        st.success("Horas actualizadas correctamente" if res else "No se pudo actualizar las horas")

# Gestionar margen de contrato
st.header("💰 Gestión de Margen de Contrato")
id_margen = st.text_input("ID de proyecto para margen de contrato")
yyyy_mm = st.text_input("Año-Mes (YYYY-MM) para margen de contrato")
if id_margen and yyyy_mm:
    margen_contrato = get_margen_contrato(id_margen, yyyy_mm)
    if margen_contrato is not None:
        st.write(f"Margen de contrato para {yyyy_mm}: {margen_contrato}")
    nuevo_margen = st.number_input("Nuevo margen de contrato", min_value=0.0, value=0.0, format="%.2f")
    if st.button("Actualizar margen de contrato"):
        res = set_margen_contrato(id_margen, yyyy_mm, nuevo_margen)
        st.success("Margen de contrato actualizado correctamente" if res else "No se pudo actualizar el margen de contrato")
