import streamlit as st
import os

# Configuración de la página en modo ancho para que aproveche todo el diseño del HTML
st.set_page_config(
    page_title="Gstión Inmobiliaria",
    page_icon="📊",
    layout="wide"
)

# Función para cargar y mostrar el archivo HTML
def load_html():
    # Busca el archivo dashboard.html en la misma carpeta
    html_file = "dashboard.html"
    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as f:
            html_content = f.read()
        # Renderiza el HTML y CSS original dentro de Streamlit
        st.components.v1.html(html_content, height=900, scrolling=True)
    else:
        st.error("No se encontró el archivo 'dashboard.html' en el repositorio. Por favor, asegúrate de subirlo.")

# Ejecutar la vista de HTML
load_html()
