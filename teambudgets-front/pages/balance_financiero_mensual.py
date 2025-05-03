import streamlit as st
from datetime import datetime
from components.sidebar import sidebar_config
from utils.objectApiCall import *
# Configuración inicial
st.set_page_config(page_title="Balance Financiero", layout="wide")
sidebar_config()


# --- Render: Cabecera y selección ---
def render_encabezado():
    st.title("Balance Financiero Mensual")

    nombre_balance = st.text_input("Nombre del balance", placeholder="Ej: Balance Proyecto A")

    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    mes_actual = datetime.now().month
    mes = st.selectbox("Mes", meses, index=mes_actual - 1)

    año_actual = datetime.now().year
    años = list(range(año_actual - 2, año_actual + 2))[::-1]
    año = st.selectbox("Año", años, index=años.index(año_actual))

    return nombre_balance, mes, año, meses

# --- Render: Gastos por trabajador ---
def render_gastos(item, idx, trabajadores, mes, año, meses):
    st.markdown("#### Trabajadores asociados")

    if "gastos" not in item:
        item["gastos"] = []

    for g_idx, gasto in enumerate(item["gastos"]):
        background_color = f"background-color: rgba({(g_idx * 50) % 255}, {(g_idx * 100) % 255}, {(g_idx * 150) % 255}, 0.1);"
        with st.container():
            st.markdown(f'<div style="{background_color} padding: 10px; border-radius: 5px;">', unsafe_allow_html=True)

            nombres_trabajadores = [t["nombre"] for t in trabajadores]
            trabajador_idx = st.selectbox(f"Trabajador", nombres_trabajadores, key=f"trabajador_sel_{idx}_{g_idx}")
            trabajador = trabajadores[nombres_trabajadores.index(trabajador_idx)]

            horas_incurridas = st.number_input("Horas incurridas", min_value=0.0, step=0.5,
                                               value=gasto.get("horas", 0.0), key=f"horas_gasto_{idx}_{g_idx}")

            mes_num = meses.index(mes) + 1
            mes_str = f"{año}-{mes_num:02d}"

            dedicacion = trabajador.get("dedicacion-mensual", {}).get(mes_str, {"laborables": 0, "vacaciones": 0})
            dias_imputables = dedicacion["laborables"] - dedicacion["vacaciones"]
            horas_imputables = dias_imputables * get_horas_jornada()

            coste_hora = trabajador.get("coste-hora-mensual", {}).get(mes_str, 48.5)
            coste_total = round(horas_incurridas * coste_hora, 2)
            gasto_desc = f"{trabajador['nombre']} ({horas_incurridas} h x {coste_hora} €/h)"

            item["gastos"][g_idx] = {
                "trabajador_id": trabajador["_id"],
                "nombre": trabajador["nombre"],
                "horas": horas_incurridas,
                "desc": gasto_desc,
                "valor": coste_total
            }

            st.markdown(f"**Días imputables:** {dias_imputables}")
            st.markdown(f"**Horas imputables (estimadas):** {horas_imputables}")
            st.markdown(f"**Coste hora:** {coste_hora} €")
            st.markdown(f"**Coste total:** {coste_total:.2f} €")

            if st.button(f"Eliminar trabajador {g_idx + 1}", key=f"remove_gasto_{idx}_{g_idx}"):
                del item["gastos"][g_idx]

            st.markdown("</div>", unsafe_allow_html=True)

    if st.button("➕ Añadir trabajador", key=f"add_gasto_{idx}"):
        item["gastos"].append({
            "trabajador_id": "",
            "nombre": "",
            "horas": 0.0,
            "desc": "",
            "valor": 0.0
        })

# --- Render: Ítem individual ---
def render_item(item, idx, proyectos, trabajadores, mes, año, meses):
    st.markdown(f"### Ítem {idx + 1}")
    col_ingreso, col_gasto = st.columns(2)

    with col_ingreso:
        tipo_ingreso = st.radio("Tipo de ingreso", ["manual", "proyecto"], key=f"tipo_ingreso_{idx}",
                                index=0 if item["tipo_ingreso"] == "manual" else 1)
        item["tipo_ingreso"] = tipo_ingreso

        if tipo_ingreso == "manual":
            ingreso_desc = st.text_input("Descripción ingreso", item["ingreso_desc"], key=f"ingreso_desc_{idx}")
            ingreso_val = st.number_input("Monto ingreso (€)", value=item["ingreso_val"], key=f"ingreso_val_{idx}")
        else:
            proyecto_nombres = [p["nombre"] for p in proyectos]
            proyecto_idx = next((i for i, p in enumerate(proyectos) if p["_id"] == item["proyecto_id"]), 0)
            proyecto_sel = st.selectbox("Seleccionar proyecto", proyecto_nombres, index=proyecto_idx, key=f"proyecto_sel_{idx}")
            proyecto = proyectos[proyecto_nombres.index(proyecto_sel)]

            horas_input = st.number_input("Horas a contabilizar", min_value=0.0, step=0.5,
                                          value=item["horas"], key=f"horas_{idx}")
            margen = proyecto["margen-contrato"]["margen"]
            horas_venta = proyecto["horas"]["venta"]
            horas_consumidas = proyecto["horas"]["consumidas"]
            horas_disponibles = (1 - margen) * horas_venta - horas_consumidas
            horas_restantes = horas_disponibles - horas_input
            ingreso_val = round(horas_input * get_ultima_tarifa(), 2)
            avance_total = (horas_consumidas + horas_input) / (horas_venta * (1 - margen)) * 100 if horas_venta > 0 else 0

            st.markdown(f"**Máximo horas permitidas:** {horas_disponibles:.2f}")
            st.markdown(f"**Horas restantes:** {horas_restantes:.2f}")
            st.markdown(f"**Avance del proyecto:** {avance_total:.2f} %")

            ingreso_desc = f"{proyecto['nombre']} ({horas_input} h x {get_ultima_tarifa()} €)"

            item["proyecto_id"] = proyecto["_id"]
            item["horas"] = horas_input

        item["ingreso_desc"] = ingreso_desc
        item["ingreso_val"] = ingreso_val

    with col_gasto:
        render_gastos(item, idx, trabajadores, mes, año, meses)

    ingreso_val = item["ingreso_val"]
    gasto_val = sum(g["valor"] for g in item["gastos"])
    diferencia = ingreso_val - gasto_val
    color = "green" if diferencia >= 0 else "red"
    st.markdown(f"<div style='color:{color}; font-weight:bold;'>Diferencia: {diferencia:.2f} €</div>", unsafe_allow_html=True)
    st.markdown("---")
    return diferencia

# --- Main Page Render ---
def render_page():
    nombre_balance, mes, año, meses = render_encabezado()

    if "registro_items" not in st.session_state:
        st.session_state.registro_items = []

    if st.button("➕ Añadir ítem"):
        st.session_state.registro_items.append({
            "tipo_ingreso": "manual",
            "ingreso_desc": "",
            "ingreso_val": 0.0,
            "proyecto_id": "",
            "horas": 0.0,
            "gastos": []
        })

    st.markdown("---")

    proyectos = get_proyectos()
    trabajadores = get_trabajadores()
    total_balance = 0.0

    for idx, item in enumerate(st.session_state.registro_items):
        diferencia = render_item(item, idx, proyectos, trabajadores, mes, año, meses)
        total_balance += diferencia

    st.subheader(f"Balance Total para {nombre_balance or 'Balance sin nombre'} - {mes} {año}")
    color_total = "green" if total_balance >= 0 else "red"
    st.markdown(f"<div style='color:{color_total}; font-size:24px; font-weight:bold;'>{total_balance:.2f} €</div>", unsafe_allow_html=True)

# Ejecutar
render_page()
