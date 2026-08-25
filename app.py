import os
import streamlit as st

# Configuración de la página en modo ancho
st.set_page_config(
    page_title="Gestión Inmobiliaria", page_icon="📊", layout="wide"
)

# ==========================================
# ESTILOS CSS PARA BLOQUEAR EL SCROLL DE STREAMLIT
# ==========================================
st.markdown(
    """
    <style>
    /* Ocultar el scroll y ajustar márgenes de la página principal de Streamlit */
    .stApp {
        overflow: hidden !important;
    }
    
    /* Eliminar padding excesivo del contenedor principal para que el dashboard ocupe toda la vista */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100% !important;
    }
    
    /* Asegurar que el iframe o componente HTML maneje su propio espacio */
    iframe {
        display: block;
        width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# FUNCIÓN PARA CARGAR EL DASHBOARD HTML
# ==========================================
def load_html():
    html_file = "dashboard.html"
    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # Renderiza el HTML con scrolling=True para que el scroll viva 100% dentro del iframe
        st.components.v1.html(
            html_content, 
            height=850,       # Altura fija o ajustada al alto de tu pantalla en modo wide
            scrolling=True    # Activa la barra de desplazamiento únicamente en tu dashboard
        )
    else:
        st.error(
            "No se encontró el archivo 'dashboard.html' en el repositorio. Por favor, asegúrate de subirlo."
        )

# Ejecutar la vista de HTML
load_html()
