import streamlit as st
from components.sidebar import sidebar_config 

st.set_page_config(page_title="Panel de Control", layout="wide")
sidebar_config()
st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='font-size: 3em;'>💰 Team Budgets</h1>
        <p style='font-size: 1.2em; color: gray;'>Servidor de objetos presupuestarios</p>
    </div>
""", unsafe_allow_html=True)