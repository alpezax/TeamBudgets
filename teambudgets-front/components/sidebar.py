import streamlit as st
import requests
from config import API_URL

def sidebar_config():
    st.sidebar.title("Configuración")

    # 1. Obtener lista de namespaces
    try:
        response = requests.get(f"{API_URL}/data/ENTORNOS-DISPONIBLES")
        response.raise_for_status()
        namespaces_data = response.json()
        if isinstance(namespaces_data, dict):
            namespaces = namespaces_data.get("ENTORNOS-DISPONIBLES", [])
        else:
            namespaces = namespaces_data
    except Exception as e:
        st.sidebar.error("No se pudo cargar la lista de namespaces.")
        st.stop()

    # 2. Obtener namespace actual
    try:
        response = requests.get(f"{API_URL}/data/ENTORNO")
        response.raise_for_status()
        current_namespace = response.json().get("ENTORNO")
    except Exception:
        current_namespace = namespaces[0] if namespaces else None

    # 3. Establecer en session_state si no está definido
    if "ENTORNO" not in st.session_state:
        st.session_state["ENTORNO"] = current_namespace

    # 4. Callback para actualizar backend si cambia el valor
    def update_namespace():
        new_namespace = st.session_state["ENTORNO"]
        if new_namespace != current_namespace:
            try:
                response = requests.post(
                    f"{API_URL}/data",
                    json={"data": {"ENTORNO": new_namespace}}
                )
                response.raise_for_status()
                st.sidebar.success(f"Namespace actualizado a: {new_namespace}")
                #st.experimental_rerun()
            except Exception:
                st.sidebar.error("No se pudo actualizar el namespace.")

    # 5. Selector en la sidebar con callback
    st.sidebar.selectbox(
        "namespace",
        namespaces,
        index=namespaces.index(st.session_state["ENTORNO"]) if st.session_state["ENTORNO"] in namespaces else 0,
        key="ENTORNO",
        on_change=update_namespace
    )
