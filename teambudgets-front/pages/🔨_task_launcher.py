import streamlit as st
from components.sidebar import sidebar_config
from utils.taskApiCall import *
from components.auth import authenticate

st.title("Gestión de Tareas")
# Autenticación
if not authenticate():
    st.stop()


sidebar_config()
tasks = get_tasks()

if not tasks:
    st.warning("No se encontraron tareas disponibles.")
else:
    for task in tasks:
        with st.container():
            col1, col2 = st.columns([5, 1])
            col1.markdown(f"**{task}**")
            if col2.button("▶️ Ejecutar", key=f"run_{task}"):
                with st.spinner(f"Ejecutando '{task}'..."):
                    result = ejecutar_task(task)
                    if "status" in result:
                        #st.success(f"Tarea '{task}' ejecutada con éxito.")
                        st.success(str(result["message"]))
                    else:
                        st.error(f"Error al ejecutar '{task}': {result.get('detail', 'Desconocido')}")
