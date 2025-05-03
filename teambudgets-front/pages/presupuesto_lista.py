import streamlit as st
import requests
from components.sidebar import sidebar_config 
from utils.objectApiCall import get_documentos_de_coleccion, delete_document

# Configurar la barra lateral
sidebar_config()

# Título de la página
st.title("Lista de presupuestos")

# Función auxiliar para definir el emoji del estado
def estado_emoji(estado):
    emoji_map = {
        "DRAFT": "⚪",
        "FAIL": "🔴",
        "VALID": "🟢",
        "EXECUTED": "🔵",
    }
    return emoji_map.get(estado, '⚪')

def estado_tag(estado):
    color_map = {
        "DRAFT": "#B0B0B0",
        "FAIL": "#FF4B4B",
        "VALID": "#4CAF50",
        "EXECUTED": "#2196F3",
    }
    emoji_map = {
        "DRAFT": "⚪",
        "FAIL": "🔴",
        "VALID": "🟢",
        "EXECUTED": "🔵",
    }
    return f"<span style='background-color:{color_map.get(estado, '#DDD')}; \
                color:white; padding:4px 8px; border-radius:12px; font-size:0.8em;'>{emoji_map.get(estado, '⚪')} {estado}</span>"

# Obtener presupuestos
presupuestos = get_documentos_de_coleccion("presupuestos")

# Mostrar cada presupuesto
for presupuesto in presupuestos:
    año = presupuesto.get("año")
    mes = presupuesto.get("mes")
    nombre = presupuesto.get("nombre_balance")
    estado = presupuesto.get("estado")
    presupuesto_id = presupuesto["_id"]

    # Crear el título con el estado y emoji dentro del expander
    expander_title = f"{año} - {mes} | {nombre}        {estado_emoji(estado)} {estado}"

    # Crear el expander
    with st.expander(expander_title, expanded=False):
        # Mostrar el título dentro del expander en letras grandes
        st.markdown(f"### {año} - {mes} | {nombre} {estado_tag(estado)}", unsafe_allow_html=True)

        # Usar columnas para colocar acciones y estado
        col1, col2 = st.columns([4, 1])

        with col1:
            st.markdown(estado_tag(estado), unsafe_allow_html=True)

        with col2:
            if estado == "DRAFT":
                st.button("✅ Validar", key=f"validar_{presupuesto_id}")
            elif estado == "VALID":
                st.button("🚀 Ejecutar", key=f"ejecutar_{presupuesto_id}")

            if estado != "EXECUTED":
                if st.button("❌ Eliminar", key=f"eliminar_{presupuesto_id}"):
                    response = delete_document("presupuestos", id=presupuesto_id)
                    if response.get("success"):
                        st.success("Presupuesto eliminado con éxito.")
                    else:
                        st.error("Hubo un error al eliminar el presupuesto.")
            else:
                st.markdown("🔒 No se puede eliminar un presupuesto ejecutado.")

        st.json(presupuesto)
