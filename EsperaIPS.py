import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

# Título de la app
st.title("🚑 Análisis de Eficiencia en Tiempos de Espera - IPS Colombia 2016-2021")

# Cargar datos de la API
@st.cache_data
def load_data():
    url = "https://www.datos.gov.co/api/v3/views/thui-g47e/query.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['data'], columns=[col['name'] for col in data['meta']['view-columns']])
        # Ajusta nombres de columnas basados en estructura típica (id, fecha, IPS, departamento, indicador, valor, etc.)
        # Asume columnas comunes: 'codigo_ips', 'nombre_ips', 'departamento', 'ano', 'mes', 'indicador', 'tiempo_espera'
        df['valor'] = pd.to_numeric(df['valor'], errors='coerce')  # Ajusta 'valor' al campo numérico real
        df['fecha'] = pd.to_datetime(df['fecha'])  # Ajusta campo fecha
        df = df[(df['ano'] >= 2016) & (df['ano'] <= 2021)]
        return df
    else:
        st.error("Error al cargar datos de la API. Verifica la URL.")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# Filtros interactivos
col1, col2, col3 = st.columns(3)
with col1:
    dept = st.multiselect("Departamento", options=df['departamento'].unique(), default=df['departamento'].unique())
with col2:
    ano = st.multiselect("Año", options=df['ano'].unique(), default=df['ano'].unique())
with col3:
    tipo = st.selectbox("Tipo de Servicio", options=['Medicina General', 'Odontología General', 'Triage 2 Urgencias'])

df_filt = df[(df['departamento'].isin(dept)) & (df['ano'].isin(ano)) & (df['indicador'].str.contains(tipo, na=False))]

## Estadísticas Descriptivas
col_a, col_b = st.columns(2)
with col_a:
    st.metric("Tiempo Promedio Espera", f"{df_filt['valor'].mean():.2f} días")
with col_b:
    st.metric("Tiempo Máximo", f"{df_filt['valor'].max():.2f} días")

## Visualización: Tendencia Temporal
fig_line = px.line(df_filt, x='fecha', y='valor', color='nombre_ips', title="Evolución Tiempos de Espera")
fig_line.update_layout(xaxis_title="Fecha", yaxis_title="Días de Espera")
st.plotly_chart(fig_line, use_container_width=True)

## Visualización: Boxplot por IPS (Eficiencia Comparativa)
fig_box = px.box(df_filt, x='nombre_ips', y='valor', color='departamento', title="Distribución Tiempos por IPS")
fig_box.update_layout(xaxis_title="IPS", yaxis_title="Días de Espera")
st.plotly_chart(fig_box, use_container_width=True)

## Mapa de Calor: Promedios por Año y Departamento
pivot = df_filt.pivot_table(values='valor', index='departamento', columns='ano', aggfunc='mean')
fig_heat = px.imshow(pivot, title="Mapa Calor Promedios por Año/Departamento", aspect="auto")
st.plotly_chart(fig_heat, use_container_width=True)

## Tabla de Datos
st.subheader("Datos Filtrados")
st.dataframe(df_filt)
