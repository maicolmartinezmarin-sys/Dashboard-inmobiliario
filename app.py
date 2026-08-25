import streamlit as st
import pandas as pd
from supabase import create_client, Client

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Proyectos Sísmicos",
    page_icon="📊",
    layout="wide"
)

# --- CONFIGURACIÓN DE SUPABASE ---
# (Puedes usar st.secrets para mayor seguridad en producción)
SUPABASE_URL = "https://eqzcjwnqbyznqdqvlpme.supabase.co"
SUPABASE_KEY = "sb_publishable_kQF1GxM-V_xt1vNGXMCLnw_KluAXT13"

@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase: Client = init_connection()

# --- FUNCIONES DE CARGA Y ACTUALIZACIÓN ---
def load_data(table_name):
    response = supabase.table(table_name).select("*").order("id").execute()
    return pd.DataFrame(response.data)

def update_supabase_row(table_name, row_id, column, value):
    try:
        supabase.table(table_name).update({column: value}).eq("id", row_id).execute()
    except Exception as e:
        st.error(f"Error al actualizar la base de datos: {e}")

# Cargar datos desde Supabase
df_area = load_data("proyectos_area")
df_intervencion = load_data("proyectos_intervencion")
df_predios = load_data("proyectos_predios")
df_juridico = load_data("proyectos_juridico")
df_valoracion = load_data("proyectos_valoracion")

# --- TÍTULO Y NAVEGACIÓN ---
st.title("📊 Dashboard de Proyectos Sísmicos - Colaborativo")
st.markdown("Cualquier cambio realizado en las tablas se sincroniza y guarda automáticamente en Supabase.")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📍 Áreas", 
    "📈 Intervención", 
    "🏠 Predios", 
    "⚖️ Análisis Jurídico", 
    "💰 Valoración"
])

# ==========================================
# PESTAÑA 1: ÁREAS
# ==========================================
with tab1:
    st.subheader("Cuadro General de Áreas por Proyecto")
    
    total_area = df_area["area"].sum()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Área Total Proyecto", f"{total_area:.1f} km²")
    
    # Editor interactivo de Streamlit
    edited_area = st.data_editor(
        df_area,
        column_config={
            "id": st.column_config.NumberColumn("ID", disabled=True),
            "bloque": st.column_config.TextColumn("Proyecto / Bloque", disabled=True),
            "area": st.column_config.NumberColumn("Área (km²)", format="%.1f km²")
        },
        hide_index=True,
        key="editor_area"
    )
    
    # Si el usuario edita la tabla, guardamos los cambios en Supabase
    if not edited_area.equals(df_area):
        for index, row in edited_area.iterrows():
            if row["area"] != df_area.loc[index, "area"]:
                update_supabase_row("proyectos_area", int(row["id"]), "area", float(row["area"]))
        st.rerun()

# ==========================================
# PESTAÑA 2: INTERVENCIÓN
# ==========================================
with tab2:
    st.subheader("Matriz de Intervención por Bloque")
    
    edited_intervencion = st.data_editor(
        df_intervencion,
        column_config={
            "id": st.column_config.NumberColumn("ID", disabled=True),
            "bloque": st.column_config.TextColumn("Bloque", disabled=True),
            "total_predios": st.column_config.NumberColumn("Total Predios"),
            "delimitado": st.column_config.NumberColumn("Delimitado"),
            "permisado": st.column_config.NumberColumn("Permisado"),
            "sin_intervencion": st.column_config.NumberColumn("Sin Intervención")
        },
        hide_index=True,
        key="editor_intervencion"
    )
    
    if not edited_intervencion.equals(df_intervencion):
        for index, row in edited_intervencion.iterrows():
            for col in ["total_predios", "delimitado", "permisado", "sin_intervencion"]:
                if row[col] != df_intervencion.loc[index, col]:
                    update_supabase_row("proyectos_intervencion", int(row["id"]), col, int(row[col]))
        st.rerun()

# ==========================================
# PESTAÑA 3: PREDIOS
# ==========================================
with tab3:
    st.subheader("Matriz de Caracterización de Predios")
    
    edited_predios = st.data_editor(
        df_predios,
        column_config={
            "id": st.column_config.NumberColumn("ID", disabled=True),
            "bloque": st.column_config.TextColumn("Proyecto", disabled=True),
            "con_fmi": st.column_config.NumberColumn("Con FMI"),
            "sin_fmi": st.column_config.NumberColumn("Sin FMI"),
            "derivadas_fmi": st.column_config.NumberColumn("Derivadas FMI"),
            "nuevos_ocupantes": st.column_config.NumberColumn("Nuevos Ocupantes"),
            "nuevos_poseedor": st.column_config.NumberColumn("Nuevos Poseedor")
        },
        hide_index=True,
        key="editor_predios"
    )
    
    if not edited_predios.equals(df_predios):
        for index, row in edited_predios.iterrows():
            for col in ["con_fmi", "sin_fmi", "derivadas_fmi", "nuevos_ocupantes", "nuevos_poseedor"]:
                if row[col] != df_predios.loc[index, col]:
                    update_supabase_row("proyectos_predios", int(row["id"]), col, int(row[col]))
        st.rerun()

# ==========================================
# PESTAÑA 4: ANÁLISIS JURÍDICO
# ==========================================
with tab4:
    st.subheader("Análisis Jurídico de Áreas")
    
    edited_juridico = st.data_editor(
        df_juridico,
        column_config={
            "id": st.column_config.NumberColumn("ID", disabled=True),
            "bloque": st.column_config.TextColumn("Proyecto", disabled=True),
            "area_bloque": st.column_config.NumberColumn("Área Bloque (km²)", format="%.2f"),
            "area_fmi": st.column_config.NumberColumn("Área FMI (km²)", format="%.2f"),
            "estudios": st.column_config.NumberColumn("Estudios Jurídicos")
        },
        hide_index=True,
        key="editor_juridico"
    )
    
    if not edited_juridico.equals(df_juridico):
        for index, row in edited_juridico.iterrows():
            for col in ["area_bloque", "area_fmi", "estudios"]:
                if row[col] != df_juridico.loc[index, col]:
                    val = float(row[col]) if col != "estudios" else int(row[col])
                    update_supabase_row("proyectos_juridico", int(row["id"]), col, val)
        st.rerun()

# ==========================================
# PESTAÑA 5: VALORACIÓN
# ==========================================
with tab5:
    st.subheader("Valoración de Intervención")
    
    tarifa = st.number_input("Configuración de Tarifa Global por m² ($)", value=900.0, step=50.0)
    
    edited_valoracion = st.data_editor(
        df_valoracion,
        column_config={
            "id": st.column_config.NumberColumn("ID", disabled=True),
            "bloque": st.column_config.TextColumn("Proyecto", disabled=True),
            "salvos_m2": st.column_config.NumberColumn("Salvos (m²)", format="%.2f"),
            "receptoras_m2": st.column_config.NumberColumn("Receptoras (m²)", format="%.2f")
        },
        hide_index=True,
        key="editor_valoracion"
    )
    
    if not edited_valoracion.equals(df_valoracion):
        for index, row in edited_valoracion.iterrows():
            for col in ["salvos_m2", "receptoras_m2"]:
                if row[col] != df_valoracion.loc[index, col]:
                    update_supabase_row("proyectos_valoracion", int(row["id"]), col, float(row[col]))
        st.rerun()
