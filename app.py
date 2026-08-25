import os
import streamlit as st

# Configuración de la página en modo ancho
st.set_page_config(
    page_title="Gestión Inmobiliaria", page_icon="📊", layout="wide"
)

# ==========================================
# ESTILOS CSS PARA ANULAR EL SCROLL NATIVO
# ==========================================
st.markdown(
    """
    <style>
    /* Ocultar barra de desplazamiento general en el body y contenedores de Streamlit */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"] {
        overflow: hidden !important;
        height: 100% !important;
    }
    
    /* Eliminar padding superior e inferior excesivos de la vista principal */
    [data-testid="stMainBlockContainer"] {
        padding-top: 0.5rem !important;
        padding-bottom: 0rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    /* Asegurar que el menú superior o footer de Streamlit no fuercen altura extra */
    header {
        visibility: hidden;
        height: 0px;
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
        
        # Renderiza el HTML con altura calculada para ocupar la pantalla completa sin desbordar
        st.components.v1.html(
            html_content, 
            height=900,       # Puedes ajustar este valor si notas que queda un espacio abajo
            scrolling=True    # El scroll se queda exclusivamente dentro de tu HTML
        )
    else:
        st.error(
            "No se encontró el archivo 'dashboard.html' en el repositorio. Por favor, asegúrate de subirlo."
        )

# Ejecutar la vista de HTML
load_html()
