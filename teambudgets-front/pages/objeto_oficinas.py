import streamlit as st
from components.sidebar import sidebar_config 
from utils.objectApiCall import *

st.title("Gestión de Oficinas")
sidebar_config()

# Mostrar todas las oficinas
st.header("📋 Oficinas registradas")
oficinas = get_oficinas()
for oficina in oficinas:
    with st.expander(f"{oficina['ciudad']} - {oficina['tipo']} ({oficina['simbolo']})"):
        st.json(oficina)

# Crear nueva oficina
st.header("➕ Crear Oficina")
with st.form("crear_oficina"):
    ciudad = st.text_input("Ciudad")
    tipo = st.text_input("Tipo")
    simbolo = st.text_input("Símbolo")
    submitted = st.form_submit_button("Crear")
    if submitted:
        res = crear_oficina(ciudad, tipo, simbolo)
        st.success(f"Oficina creada: {res.get('id')}")

# Actualizar oficina
st.header("✏️ Actualizar Oficina")
id_update = st.text_input("ID de oficina a actualizar")
if id_update:
    oficina = get_oficina(id_update)
    if oficina:
        ciudad_u = st.text_input("Ciudad", oficina.get("ciudad"))
        tipo_u = st.text_input("Tipo", oficina.get("tipo"))
        simbolo_u = st.text_input("Símbolo", oficina.get("simbolo"))
        if st.button("Actualizar"):
            res = actualizar_oficina(id_update, ciudad_u, tipo_u, simbolo_u)
            st.success(res.get("message"))

# Eliminar oficina
st.header("🗑️ Eliminar Oficina")
id_delete = st.text_input("ID de oficina a eliminar")
if st.button("Eliminar"):
    res = eliminar_oficina(id_delete)
    st.warning(res.get("message"))

# Gestión mejorada de días laborables
st.header("📆 Días laborables por mes")

id_dl = st.text_input("ID de oficina", key="dias_laborables_id")

st.subheader("➕ Añadir mes y año")
col1, col2, col3 = st.columns(3)

with col1:
    mes_nombre = st.selectbox("Mes", [
        "01 - Enero", "02 - Febrero", "03 - Marzo", "04 - Abril", "05 - Mayo", "06 - Junio",
        "07 - Julio", "08 - Agosto", "09 - Septiembre", "10 - Octubre", "11 - Noviembre", "12 - Diciembre"
    ])

with col2:
    anio = st.text_input("Año", key="anio_dl")

with col3:
    dias = st.number_input("Días laborables", min_value=0, max_value=31, key="dias_dl", step=1)

if "dl_data" not in st.session_state:
    st.session_state.dl_data = []

if st.button("➕ Añadir mes"):
    if anio and mes_nombre:
        mes = mes_nombre.split(" - ")[0]
        yyyy_mm = f"{anio}-{mes}"
        ya_existe = any(item["yyyy_mm"] == yyyy_mm for item in st.session_state.dl_data)
        if ya_existe:
            st.warning(f"Ya se añadió {yyyy_mm}.")
        else:
            st.session_state.dl_data.append({"yyyy_mm": yyyy_mm, "dias": dias})
    else:
        st.warning("Debes indicar el año y seleccionar un mes.")

# Mostrar tabla editable
if st.session_state.dl_data:
    st.subheader("🗂️ Días laborables añadidos")
    for i, row in enumerate(st.session_state.dl_data):
        col1, col2, col3 = st.columns([3, 2, 1])
        col1.write(row["yyyy_mm"])
        col2.write(f"{row['dias']} días")
        if col3.button("❌", key=f"del_{i}"):
            st.session_state.dl_data.pop(i)
            st.experimental_rerun()

# Enviar todo
if st.button("📤 Guardar días laborables en API"):
    if not id_dl:
        st.error("Debes indicar el ID de la oficina.")
    else:
        success = True
        for item in st.session_state.dl_data:
            res = set_dias_laborables(id_dl, item["yyyy_mm"], item["dias"])
            if "message" not in res:
                success = False
                st.error(f"Error al guardar {item['yyyy_mm']}: {res}")
        if success:
            st.success("Todos los días laborables fueron actualizados.")
            st.session_state.dl_data = []


##** Actualiza
st.header("✏️ Actualizar días laborables existentes")

id_oficina_update = st.text_input("ID de oficina para actualizar días", key="actualizar_id_dl")

if id_oficina_update:
    oficina_data = get_oficina(id_oficina_update)
    if "_id" in oficina_data:
        st.success(f"Oficina: {oficina_data.get('ciudad')} ({oficina_data.get('simbolo')})")

        dias_laborables_actuales = get_dias_laborables_all(id_oficina_update)

        if not dias_laborables_actuales:
            st.info("No hay días laborables registrados para esta oficina.")
        else:
            st.subheader("📅 Editar días laborables por mes")
            actualizaciones = {}

            for i, (yyyy_mm, dias) in enumerate(oficina_data.get("dias-laborables", {}).items()):
                if not (isinstance(yyyy_mm, str) and len(yyyy_mm) == 7 and yyyy_mm[4] == "-"):
                    continue  # Salta claves como "detail"

                col1, col2 = st.columns([2, 1])
                col1.write(yyyy_mm)
                valor_defecto = int(dias) if isinstance(dias, int) or (isinstance(dias, str) and dias.isdigit()) else 0
                nuevo_valor = col2.number_input(
                    f"Días para {yyyy_mm}", min_value=0, max_value=31, value=valor_defecto, key=f"edit_dl_{i}"
                )
                actualizaciones[yyyy_mm] = nuevo_valor

            if actualizaciones and st.button("💾 Guardar cambios"):
                errores = []
                for yyyy_mm, nuevo_valor in actualizaciones.items():
                    res = set_dias_laborables(id_oficina_update, yyyy_mm, nuevo_valor)
                    if "message" not in res:
                        errores.append((yyyy_mm, res))
                if errores:
                    for yyyy_mm, err in errores:
                        st.error(f"❌ Error en {yyyy_mm}: {err}")
                else:
                    st.success("✅ Todos los días laborables fueron actualizados correctamente.")
    else:
        st.error("❌ Oficina no encontrada.")
