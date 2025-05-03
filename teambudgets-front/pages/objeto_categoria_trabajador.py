import streamlit as st
from components.sidebar import sidebar_config 
from utils.objectApiCall import *


# Título de la aplicación
st.title("Gestión de Categorías de Trabajador")
sidebar_config()

# Mostrar todas las categorías
st.header("📋 Categorías de Trabajadores")
categorias = get_categorias()
for categoria in categorias:
    with st.expander(f"{categoria['nombre']} (Simbolo: {categoria['simbolo']})"):
        st.json(categoria)

# Crear nueva categoría
st.header("➕ Crear Categoría de Trabajador")
with st.form("crear_categoria"):
    nombre = st.text_input("Nombre de la Categoría")
    clase = st.text_input("Clase de la Categoría")
    simbolo = st.text_input("Símbolo de la Categoría")
    submitted = st.form_submit_button("Crear Categoría")
    if submitted:
        res = crear_categoria(nombre, clase, simbolo)
        st.success(f"Categoría creada con ID: {res['id']}")

# Actualizar categoría
st.header("✏️ Actualizar Categoría de Trabajador")
id_update = st.text_input("ID de categoría a actualizar")
if id_update:
    categoria = get_categoria_by_id(id_update)
    if categoria:
        nombre_u = st.text_input("Nombre", categoria.get("nombre"))
        clase_u = st.text_input("Clase", categoria.get("clase"))
        simbolo_u = st.text_input("Símbolo", categoria.get("simbolo"))
        if st.button("Actualizar"):
            res = actualizar_categoria(id_update, nombre_u, clase_u, simbolo_u)
            st.success("Categoría actualizada correctamente" if res else "No se pudo actualizar la categoría")

# Eliminar categoría
st.header("🗑️ Eliminar Categoría")
id_delete = st.text_input("ID de categoría a eliminar")
if st.button("Eliminar"):
    res = eliminar_categoria(id_delete)
    st.warning("Categoría eliminada correctamente" if res else "No se pudo eliminar la categoría")

# Gestionar CSR de una categoría
st.header("💰 Gestionar CSR de Categoría")
id_csr = st.text_input("ID de categoría para CSR")
simbolo_csr = st.text_input("Símbolo de categoría para obtener CSR")
if id_csr:
    csr_categoria = get_csr_by_fecha(id_csr, "2025-04")  # Ejemplo de fecha "yyyy-mm"
    if csr_categoria:
        st.write(f"CSR para {id_csr}: {csr_categoria}")
    nuevo_csr = st.number_input("Nuevo valor CSR", min_value=0.0, value=0.0, format="%.2f")
    if st.button("Actualizar CSR"):
        res = actualizar_csr(id_csr, "2025-04", nuevo_csr)
        st.success("CSR actualizado correctamente" if res else "No se pudo actualizar CSR")

# Consultar CSR por símbolo
st.header("🔍 Consultar CSR Último por Símbolo")
simbolo = st.text_input("Símbolo de categoría para consultar último CSR")
if simbolo:
    csr_ultimo = get_ultimo_csr(simbolo)
    if csr_ultimo:
        st.write(f"Último CSR para {simbolo}: {csr_ultimo}")
    else:
        st.warning("No se encontró CSR para este símbolo.")
