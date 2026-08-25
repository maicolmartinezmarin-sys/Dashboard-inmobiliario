import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
from st_supabase_connection import SupabaseConnection

# Configuración inicial de la página
st.set_page_config(page_title="GESTIÓN INMOBILIARIA", layout="wide")

# Conexión con Supabase
supabase_conn = st.connection("supabase", type=SupabaseConnection)

# 1. Función para obtener la tarifa guardada en Supabase
def cargar_tarifa():
    try:
        res = supabase_conn.table("configuracion").select("tarifa_m2").eq("id", 1).execute()
        return float(res.data[0]["tarifa_m2"]) if res.data else 900.0
    except Exception:
        return 900.0  # Valor por defecto en caso de falla de conexión

# 2. Función para actualizar la tarifa en Supabase
def actualizar_tarifa(nueva_tarifa):
    supabase_conn.table("configuracion").update({"tarifa_m2": nueva_tarifa}).eq("id", 1).execute()

# Título Principal
st.title("🏗️ GESTIÓN INMOBILIARIA - Exploración Sísmica")
st.subheader("Proyectos LLANOS 95 3D, LLA111 3D SUR y LLA111 3D NORTE")

# Control de Tarifa Global
tarifa_actual = cargar_tarifa()

with st.container():
    st.info("💡 **Configuración de Tarifa Global Centralizada:** El valor que modifiques aquí se actualizará en tiempo real para todos los usuarios que estén viendo el dashboard.")
    col_input, col_btn = st.columns([3, 1])
    
    with col_input:
        nueva_tarifa = st.number_input("Tarifa por m² ($ COP):", value=tarifa_actual, step=50.0)
    
    with col_btn:
        st.write(" ")
        st.write(" ")
        if st.button("💾 Guardar Cambio Global"):
            actualizar_tarifa(nueva_tarifa)
            st.success("¡Tarifa actualizada para todos los usuarios!")
            st.rerun()

st.divider()

# Datos de Intervención
datos_intervencion = [
    {"Proyecto": "LLA 95 3D", "Salvos_m2": 2631153.92, "Receptoras_m2": 1251249.82},
    {"Proyecto": "LLA111 3D South", "Salvos_m2": 1204490.73, "Receptoras_m2": 768473.37},
    {"Proyecto": "LLA111 North 3D", "Salvos_m2": 2823848.31, "Receptoras_m2": 1616777.44}
]

df = pd.DataFrame(datos_intervencion)
df["Valor_Salvos"] = df["Salvos_m2"] * tarifa_actual
df["Valor_Receptoras"] = df["Receptoras_m2"] * tarifa_actual
df["Total_Intervencion"] = df["Valor_Salvos"] + df["Valor_Receptoras"]

# Tarjetas KPI Native Streamlit
k1, k2, k3 = st.columns(3)
k1.metric("Área Salvos Total", f"{(df['Salvos_m2'].sum() / 1e6):,.2f} km²")
k2.metric("Área Receptoras Total", f"{(df['Receptoras_m2'].sum() / 1e6):,.2f} km²")
k3.metric("Presupuesto Total Global", f"$ {df['Total_Intervencion'].sum():,.2f}")

st.divider()

# Gráfico de Barras con Plotly
fig = px.bar(
    df, 
    x="Proyecto", 
    y=["Valor_Salvos", "Valor_Receptoras"], 
    title=f"Valoración por Proyecto (Tarifa actual: ${tarifa_actual:,.0f}/m²)",
    labels={"value": "Costo ($ COP)", "variable": "Tipo de Intervención"},
    barmode="group"
)
st.plotly_chart(fig, use_container_width=True)

# Tabla Informativa
st.subheader("Matriz de Intervención y Costos")
st.dataframe(df.style.format({
    "Salvos_m2": "{:,.2f}",
    "Receptoras_m2": "{:,.2f}",
    "Valor_Salvos": "$ {:,.2f}",
    "Valor_Receptoras": "$ {:,.2f}",
    "Total_Intervencion": "$ {:,.2f}"
}), use_container_width=True)

st.divider()

# ==============================================================================
# INTEGRACIÓN DEL COMPONENTE HTML DENTRO DE STREAMLIT
# ==============================================================================
st.subheader("🖥️ Vista Interactiva del Dashboard HTML")

# Opción A: Cargar directamente desde tu archivo .html guardado en el mismo directorio
try:
    with open("dashboard.html", "r", encoding="utf-8") as f:
        html_code = f.read()
    
    # Se establece una altura (height) amplia de 1800px para evitar cortes
    # y scrolling=True para permitir desplazamiento suave si la ventana es más pequeña.
    components.html(html_code, height=1800, scrolling=True)

except FileNotFoundError:
    st.warning("⚠️ No se encontró el archivo `dashboard.html`. Asegúrate de guardarlo en la misma carpeta raíz del archivo Python de tu aplicación Streamlit.")
