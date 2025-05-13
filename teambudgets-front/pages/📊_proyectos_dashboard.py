import streamlit as st
from components.sidebar import sidebar_config 
import plotly.graph_objects as go
from utils.objectApiCall import *
from components.auth import authenticate


st.set_page_config(layout="wide")
st.title("Dashboard de Proyectos por Equipo")

# Autenticación
if not authenticate():
    st.stop()

sidebar_config()

# Obtener equipos y mostrar selector
equipos = get_equipos()

if not equipos:
    st.warning("No se encontraron equipos.")
else:
    opciones = {equipo["nombre"]: equipo["_id"] for equipo in equipos}
    equipo_seleccionado = st.selectbox("Selecciona un equipo", list(opciones.keys()))
    equipo_id = opciones[equipo_seleccionado]

    # Obtener proyectos del equipo seleccionado
    proyectos = get_proyectos_de_equipo_con_avance(equipo_id)

    if not proyectos:
        st.info("Este equipo no tiene proyectos asignados.")
    else:
        # CSS ajustado para asegurar que el contenedor abarque todo
        card_style = """
        <style>
        .card-title {
            font-weight: bold;
            font-size: 18px;
            margin-bottom: 6px;
        }
        .card-meta {
            font-size: 14px;
            color: #777;
        }
        </style>
        """
        st.markdown(card_style, unsafe_allow_html=True)

        cols = st.columns(3)

        for i, proyecto in enumerate(proyectos):
            nombre = proyecto.get("nombre", "Sin nombre")
            horas = proyecto.get("horas", {}).get("venta", 0)
            dinero = proyecto.get("avance", {}).get("dinero-venta", 0)
            avance = proyecto.get("avance", {}).get("porcentaje-restante", 1)
            restante = 1 - avance

            fig = go.Figure(data=[
                go.Pie(
                    values=[avance, restante],
                    labels=["Consumido", "Restante"],
                    marker_colors=["green", "red"],
                    hole=0.7,
                    textinfo='none'
                )
            ])

            fig.update_layout(
                showlegend=False,
                margin=dict(t=0, b=0, l=0, r=0),
                height=130,
                width=130,
                annotations=[dict(text=f"{round(avance * 100)}%", x=0.5, y=0.5, font_size=14, showarrow=False)]
            )

            with cols[i % 3]:
                with st.container():
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.plotly_chart(fig, use_container_width=False, key=f"chart_{i}")
                    with col2:
                        st.markdown(f"<div class='card-title'>{nombre}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='card-meta'>Horas del proyecto: {horas}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='card-meta'>Dinero del proyecto: {dinero} €</div>", unsafe_allow_html=True)
