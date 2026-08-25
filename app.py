import os
import streamlit as st

# Configuración de la página en modo ancho para que aproveche todo el diseño
st.set_page_config(
    page_title="Gestión Inmobiliaria", page_icon="📊", layout="wide"
)

# ==========================================
# ESTILOS CSS GENERALES DE LA APP (Opcional)
# ==========================================
st.markdown(
    """
    <style>
    /* Ocultar elementos predeterminados de Streamlit si quieres vista 100% limpia tipo app web */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# FUNCIÓN PARA CARGAR EL DASHBOARD HTML
# ==========================================
def load_html():
    # Busca el archivo dashboard.html en la misma carpeta
    html_file = "dashboard.html"
    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # Renderiza el HTML permitiendo el scroll nativo dentro del componente
        st.components.v1.html(
            html_content, 
            height=850,       # Altura visible del visor en píxeles (ajústala si es necesario)
            scrolling=True    # Habilita la barra de desplazamiento interna del iframe
        )
    else:
        st.error(
            "No se encontró el archivo 'dashboard.html' en el repositorio. Por favor, asegúrate de subirlo."
        )

# Ejecutar la vista de HTML
load_html()
