import streamlit as st
import streamlit.components.v1 as components

# Configuración inicial de la página a ancho completo
st.set_page_config(page_title="GESTIÓN INMOBILIARIA", layout="wide")

# Renderizado exclusivo del Dashboard HTML completo
try:
    with open("dashboard.html", "r", encoding="utf-8") as f:
        html_code = f.read()
    
    # Renderiza únicamente la interfaz interactiva HTML a pantalla completa
    components.html(html_code, height=1800, scrolling=True)

except FileNotFoundError:
    st.error("⚠️ No se encontró el archivo `dashboard.html`. Asegúrate de haberlo subido al repositorio en GitHub en la misma carpeta que `app.py`.")
