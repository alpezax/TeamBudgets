import streamlit as st
from components.sidebar import sidebar_config 
from utils.objectApiCall import *
from components.auth import authenticate

# Título de la aplicación
st.title("Gestión de Trabajadores")

# Autenticación
if not authenticate():
    st.stop()
    
sidebar_config()

# Mostrar todos los trabajadores
st.header("📋 Trabajadores registrados")
trabajadores = get_trabajadores()
for trabajador in trabajadores:
    with st.expander(f"{trabajador['nombre']} ({trabajador['alias']})"):
        st.json(trabajador)


# Crear nuevo trabajador
st.header("➕ Crear Trabajador")
with st.form("crear_trabajador"):
    nombre = st.text_input("Nombre")

    # Oficina
    oficinas = get_oficinas()
    opciones_oficinas = {f"{o['simbolo']} - {o['ciudad']} - {o['tipo']}": o["_id"] for o in oficinas}
    oficina_seleccion = st.selectbox("Oficina", list(opciones_oficinas.keys()))
    oficina_id = opciones_oficinas[oficina_seleccion]

    # Categoría
    categorias = get_categorias()
    opciones_categorias = {f"{c['simbolo']} - {c['nombre']} - {c['clase']}": c["_id"] for c in categorias}
    categoria_seleccion = st.selectbox("Categoría", list(opciones_categorias.keys()))
    categoria_id = opciones_categorias[categoria_seleccion]

    alias = st.text_input("Alias")
    tags = st.text_area("Tags (separados por comas)").split(",")
    workpool = st.text_area("Workpool (separados por comas)").split(",")
    dedicacion_mensual = {}  
    coste_hora_mensual = {}  
    submitted = st.form_submit_button("Crear")
    if submitted:
        res = crear_trabajador(nombre, oficina_id, categoria_id, alias, tags, workpool, dedicacion_mensual, coste_hora_mensual)
        st.success(f"Trabajador creado: {res}")

# Actualizar trabajador
st.header("✏️ Actualizar Trabajador")
id_update = st.text_input("ID de trabajador a actualizar")
if id_update:
    trabajador = get_trabajador(id_update)
    if trabajador:
        nombre_u = st.text_input("Nombre", trabajador.get("nombre"))

        # Oficina
        oficinas = get_oficinas()
        opciones_oficinas = {f"{o['simbolo']} - {o['ciudad']} - {o['tipo']}": o["_id"] for o in oficinas}
        oficina_default = next((k for k, v in opciones_oficinas.items() if v == trabajador.get("oficina")), None)
        oficina_seleccion = st.selectbox("Oficina", list(opciones_oficinas.keys()), index=list(opciones_oficinas.keys()).index(oficina_default) if oficina_default else 0)
        oficina_u = opciones_oficinas[oficina_seleccion]

        # Categoría
        categorias = get_categorias()
        opciones_categorias = {f"{c['simbolo']} - {c['nombre']} - {c['clase']}": c["_id"] for c in categorias}
        categoria_default = next((k for k, v in opciones_categorias.items() if v == trabajador.get("categoria")), None)
        categoria_seleccion = st.selectbox("Categoría", list(opciones_categorias.keys()), index=list(opciones_categorias.keys()).index(categoria_default) if categoria_default else 0)
        categoria_u = opciones_categorias[categoria_seleccion]

        alias_u = st.text_input("Alias", trabajador.get("alias"))
        if st.button("Actualizar"):
            data = {
                "nombre": nombre_u,
                "oficina": oficina_u,
                "categoria": categoria_u,
                "alias": alias_u
            }
            res = actualizar_trabajador(id_update, data)
            st.success(res.get("message"))

# Eliminar trabajador
st.header("🗑️ Eliminar Trabajador")
id_delete = st.text_input("ID de trabajador a eliminar")
if st.button("Eliminar"):
    res = eliminar_trabajador(id_delete)
    st.warning(res.get("message"))

# Gestión de dedicación mensual
st.header("📆 Dedicación Mensual")
id_dm = st.text_input("ID de trabajador")
yyyy_mm = st.text_input("Año-Mes (YYYY-MM)")
if st.button("Consultar dedicación mensual"):
    data = get_dedicacion_mensual(id_dm, yyyy_mm)
    st.write(data)

valor_dm = st.number_input("Nuevo valor de dedicación mensual", min_value=0)
if st.button("Actualizar dedicación mensual"):
    res = set_dedicacion_mensual(id_dm, yyyy_mm, {"work": valor_dm, "vacation": 0})
    st.success(res.get("message"))

# Gestión de coste hora mensual
st.header("💵 Coste Hora Mensual")
id_chm = st.text_input("ID de trabajador para coste-hora")
yyyy_mm_chm = st.text_input("Año-Mes (YYYY-MM) para coste-hora")
if st.button("Consultar coste hora mensual"):
    data = get_coste_hora_mensual(id_chm, yyyy_mm_chm)
    st.write(data)

valor_chm = st.number_input("Nuevo valor de coste hora mensual", min_value=0.0, format="%.2f")
if st.button("Actualizar coste hora mensual"):
    res = set_coste_hora_mensual(id_chm, yyyy_mm_chm, valor_chm)
    st.success(res.get("message"))
