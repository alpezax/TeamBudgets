import streamlit as st
from datetime import datetime
from components.sidebar import sidebar_config
from utils.objectApiCall import *
from utils.presupuestosLib import *
import copy


# Configuración inicial
st.set_page_config(page_title="Editar Presupuesto", layout="wide")
sidebar_config()

st.title("📝 Editar Presupuesto Existente")

# --- Recuperar documentos existentes ---
documentos = get_documentos_de_coleccion("presupuestos")

if not documentos:
    st.warning("No hay presupuestos guardados.")
    st.stop()

# Selector de documento
nombres = [doc.get("nombre_balance", "Sin nombre") for doc in documentos]
nombre_seleccionado = st.selectbox("Selecciona un presupuesto para editar", nombres)
documento = documentos[nombres.index(nombre_seleccionado)]

#st.subheader("Debug: Contenido del documento seleccionado")
#st.json(documento)  

# Hacer copia editable en session_state
if "registro_items" not in st.session_state or st.session_state.get("loaded_doc") != documento["_id"]:
    st.session_state.registro_items = copy.deepcopy(documento.get("imputaciones", []))
    st.session_state.loaded_doc = documento["_id"]

# Cargar datos base del documento
nombre_balance = st.text_input("Nombre del balance", value=documento.get("nombre_balance", ""))

meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
         "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
nombre_mes = documento.get("mes", "Enero")
try:
    mes_idx = meses.index(nombre_mes)
except ValueError:
    mes_idx = 0
mes = st.selectbox("Mes", meses, index=mes_idx)

año_actual = datetime.now().year
años = list(range(año_actual - 2, año_actual + 2))[::-1]
año = st.selectbox("Año", años, index=años.index(documento.get("año", año_actual)))

# Selección de equipo
equipos = get_equipos()
equipo_seleccionado = None
if equipos:
    equipo_nombres = [e["nombre"] for e in equipos]
    equipo_idx = next((i for i, e in enumerate(equipos) if e["_id"] == documento.get("equipo", {}).get("_id")), 0)
    equipo_sel = st.selectbox("Seleccionar equipo", equipo_nombres, index=equipo_idx)
    equipo_seleccionado = equipos[equipo_nombres.index(equipo_sel)]
else:
    st.warning("No hay equipos disponibles.")

# Renderizar items
st.markdown("---")
proyectos = get_proyectos()
trabajadores = get_trabajadores()
total_balance = 0.0

for idx, item in enumerate(st.session_state.registro_items):
    diferencia = render_item(item, idx, proyectos, trabajadores, mes, año, meses)
    total_balance += diferencia

# Añadir ítem
if st.button("➕ Añadir ítem"):
    st.session_state.registro_items.append({
        "tipo_ingreso": "manual",
        "ingreso_desc": "",
        "ingreso_val": 0.0,
        "proyecto_id": "",
        "horas": 0.0,
        "gastos": []
    })

# Resultado total
st.subheader(f"Balance Total para {nombre_balance or 'Sin nombre'} - {mes} {año}")
color_total = "green" if total_balance >= 0 else "red"
st.markdown(f"<div style='color:{color_total}; font-size:24px; font-weight:bold;'>{total_balance:.2f} €</div>", unsafe_allow_html=True)

# Botón Guardar
if st.button("💾 Guardar cambios"):
    if not nombre_balance.strip():
        st.error("⚠️ El balance debe tener un nombre.")
    else:
        documento_actualizado = {
            "_id": documento["_id"],  # Para indicar que es una edición
            "nombre_balance": nombre_balance,
            "mes": meses.index(mes) + 1,
            "año": año,
            "equipo": equipo_seleccionado,
            "items": st.session_state.registro_items,
        }
        response = replace_entire_document("presupuestos", documento_actualizado)
        if response.get("message") == "Documento reemplazado correctamente.":
            st.success("✅ Presupuesto actualizado correctamente.")
        else:
            st.error(f"❌ Error al guardar los cambios: {response.get('detail', 'Respuesta inesperada.')}")
