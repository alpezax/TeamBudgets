import streamlit as st
from components.sidebar import sidebar_config
from utils.objectApiCall import *
from components.auth import authenticate

st.title("Gestión de Equipos")
# Autenticación
if not authenticate():
    st.stop()
    
sidebar_config()
# Mostrar todos los equipos
st.header("📋 Equipos registrados")
equipos = get_equipos()
for equipo in equipos:
    with st.expander(f"{equipo['nombre']}"):
        st.json(equipo)

# Crear nuevo equipo
st.header("➕ Crear Equipo")
with st.form("crear_equipo"):
    nombre = st.text_input("Nombre del equipo")
    descripcion = st.text_area("Descripción")

    proyectos_disponibles = get_proyectos()
    proyectos_dict = {f"{p['nombre']} ({p['_id']})": p['_id'] for p in proyectos_disponibles}
    proyectos_seleccionados = st.multiselect("Proyectos a vincular", list(proyectos_dict.keys()))

    submitted = st.form_submit_button("Crear")
    if submitted:
        res = crear_equipo(nombre, descripcion)
        if "_id" in res:
            equipo_id = res["_id"]
            st.success(f"Equipo creado: {equipo_id}")
            for key in proyectos_seleccionados:
                res_vinc = vincular_proyecto_equipo(equipo_id, proyectos_dict[key])
                if "message" in res_vinc:
                    st.info(f"Proyecto vinculado: {key}")
                else:
                    st.warning(f"No se pudo vincular {key}")
        else:
            st.error("Error al crear equipo.")

# Actualizar equipo
st.header("✏️ Actualizar Equipo")
id_update = st.text_input("ID de equipo a actualizar")
if id_update:
    equipo = get_equipo(id_update)
    if equipo:
        nombre_u = st.text_input("Nombre", equipo.get("nombre"))
        descripcion_u = st.text_area("Descripción", equipo.get("descripcion"))
        if st.button("Actualizar"):
            res = actualizar_equipo(id_update, nombre_u, descripcion_u)
            st.success(res.get("message"))

        st.subheader("📌 Proyectos vinculados")
        proyectos_vinculados = equipo.get("proyectos", [])
        for pid in proyectos_vinculados:
            proyecto = get_proyecto(pid)
            col1, col2 = st.columns([4, 1])
            col1.write(f"{proyecto.get('nombre')} ({pid})")
            if col2.button("❌ Desvincular", key=f"desvincular_{pid}"):
                res = desvincular_proyecto_equipo(id_update, pid)
                if "message" in res:
                    st.success(res["message"])
                    st.experimental_rerun()
                else:
                    st.error(f"Error al desvincular: {res}")

        st.subheader("➕ Añadir nuevos proyectos")
        todos_proyectos = get_proyectos()
        vinculados_ids = set(proyectos_vinculados)
        disponibles = {f"{p['nombre']} ({p['_id']})": p['_id'] for p in todos_proyectos if p['_id'] not in vinculados_ids}

        if disponibles:
            nuevos = st.multiselect("Seleccionar proyectos a añadir", list(disponibles.keys()), key="add_proy")
            if st.button("📎 Vincular proyectos seleccionados"):
                for key in nuevos:
                    res = vincular_proyecto_equipo(id_update, disponibles[key])
                    if "message" in res:
                        st.info(f"Proyecto vinculado: {key}")
                    else:
                        st.warning(f"No se pudo vincular {key}")
        else:
            st.info("No hay proyectos disponibles para añadir.")

# Eliminar equipo
st.header("🗑️ Eliminar Equipo")
id_delete = st.text_input("ID de equipo a eliminar")
if st.button("Eliminar"):
    res = eliminar_equipo(id_delete)
    st.warning(res.get("message"))

# Añadir miembros con participación
st.header("👥 Añadir miembros al equipo")
id_equipo = st.text_input("ID del equipo para añadir miembros", key="add_miembros")

if id_equipo:
    if "miembros_data" not in st.session_state:
        st.session_state.miembros_data = []

    trabajadores = get_trabajadores()
    trabajadores_dict = {f"{t['nombre']} ({t['_id']})": t['_id'] for t in trabajadores}

    col1, col2 = st.columns([2, 1])
    with col1:
        trabajador_sel = st.selectbox("Seleccionar trabajador", list(trabajadores_dict.keys()))
    with col2:
        participacion = st.number_input("Participación (%)", min_value=0, max_value=100, value=100, step=5)

    if st.button("➕ Añadir miembro"):
        trabajador_id = trabajadores_dict[trabajador_sel]
        ya_existe = any(m['trabajador_id'] == trabajador_id for m in st.session_state.miembros_data)
        if ya_existe:
            st.warning("Este trabajador ya ha sido añadido.")
        else:
            st.session_state.miembros_data.append({
                "trabajador_id": trabajador_id,
                "nombre": trabajador_sel,
                "participacion": participacion
            })

    if st.session_state.miembros_data:
        st.subheader("📝 Miembros añadidos")
        for i, miembro in enumerate(st.session_state.miembros_data):
            col1, col2, col3 = st.columns([3, 2, 1])
            col1.write(miembro["nombre"])
            miembro["participacion"] = col2.number_input(
                "Participación", min_value=0, max_value=100, value=miembro["participacion"], step=5, key=f"part_{i}"
            )
            if col3.button("❌", key=f"del_miembro_{i}"):
                st.session_state.miembros_data.pop(i)
                st.experimental_rerun()

    if st.button("📤 Guardar miembros en equipo"):
        errores = []
        for miembro in st.session_state.miembros_data:
            res = añadir_miembro_equipo(id_equipo, miembro["trabajador_id"], participacion=miembro["participacion"], nombre=miembro["nombre"])
            if "message" not in res:
                errores.append((miembro["nombre"], res))
        if errores:
            for nombre, err in errores:
                st.error(f"❌ Error al añadir {nombre}: {err}")
        else:
            st.success("✅ Miembros añadidos correctamente.")
            st.session_state.miembros_data = []

# Editar participación de miembros existentes
st.header("✏️ Editar participación de miembros existentes")
id_equipo_part = st.text_input("ID del equipo", key="editar_miembros")

if id_equipo_part:
    equipo = get_equipo(id_equipo_part)
    
    st.write("Equipo recibido:", equipo)
    
    if equipo and equipo.get("miembros"):
        st.success(f"Equipo: {equipo.get('nombre')}")

        nuevas_participaciones = {}
        for i, miembro in enumerate(equipo["miembros"]):
            trabajador = get_trabajador(str(miembro["trabajador_id"]))
            if trabajador:
                nombre_trabajador = trabajador.get("nombre", "Nombre no disponible")
            else:
                nombre_trabajador = "Nombre no disponible"

            col1, col2 = st.columns([3, 1])
            col1.write(nombre_trabajador)
            valor_actual = miembro.get("participacion", 0)
            nuevas_participaciones[miembro["trabajador_id"]] = col2.number_input(
                "Nuevo %", min_value=0, max_value=100, value=int(valor_actual), step=5, key=f"edit_part_{i}"
            )

        if st.button("💾 Guardar participaciones actualizadas"):
            errores = []
            for trabajador_id, nueva_part in nuevas_participaciones.items():
                res = actualizar_participacion_miembro(id_equipo_part, trabajador_id, nueva_part, nombre=nombre_trabajador)
                if "message" not in res:
                    errores.append((trabajador_id, res))
            if errores:
                for t_id, err in errores:
                    st.error(f"❌ Error con trabajador {t_id}: {err}")
            else:
                st.success("✅ Participaciones actualizadas correctamente.")
    else:
        st.warning("No se encontraron miembros en este equipo.")
