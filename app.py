import os
import streamlit as st

# Configuración de la página en modo ancho para que aproveche todo el diseño
st.set_page_config(
    page_title="Gestión Inmobiliaria", page_icon="📊", layout="wide"
)

# ==========================================
# ESTILOS CSS PERSONALIZADOS (Contenedor con scroll)
# ==========================================
st.markdown(
    """
    <style>
    /* Contenedor flexible que se adapta al 100% del ancho del contenedor padre */
    .custom-scroll-container {
        width: 100%;
        max-height: 500px; /* Ajusta la altura máxima según lo necesites */
        overflow-y: auto;
        overflow-x: hidden; /* Evita scroll horizontal no deseado */
        padding-right: 8px;
        box-sizing: border-box; /* Asegura que el padding no rompa el ancho */
    }

    /* Estilización moderna de la barra de desplazamiento */
    .custom-scroll-container::-webkit-scrollbar {
        width: 6px;
    }

    .custom-scroll-container::-webkit-scrollbar-track {
        background: transparent;
    }

    .custom-scroll-container::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 4px;
    }

    .custom-scroll-container::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
    </style>
    """,
    unsafe_allow_html=True,
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
    st.error(
        "No se encontró el archivo 'dashboard.html' en el repositorio. Por"
        " favor, asegúrate de subirlo."
    )


# Ejecutar la vista de HTML
load_html()
