"""
🚑 Dashboard Tiempos Espera IPS Colombia - VERSIÓN PRODUCCIÓN
Compatible 100% Streamlit Cloud
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import io

# Configuración optimizada
st.set_page_config(
    page_title="🚑 Tiempos Espera IPS Colombia",
    page_icon="🚑",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_demo_data():
    """Dataset DEMO optimizado - Sin dependencias externas"""
    np.random.seed(42)
    n = 5000  # Reducido para performance
    
    departamentos = ['ANTIOQUIA', 'BOGOTÁ D.C.', 'VALLE DEL CAUCA', 'CUNDINAMARCA', 
                    'SANTANDER', 'RISARALDA']
    servicios = ['MEDICINA GENERAL', 'ODONTOLOGÍA GENERAL', 'TRIAGE 2 URG']
    ips = ['IPS CENTRAL', 'CLÍNICA MODELO', 'HOSPITAL UNIVERSITARIO', 
           'IPS METROPOLITANA', 'CLÍNICA DEL SUR']
    
    fechas = pd.date_range('2016-01-01', '2021-12-31', freq='MS')
    
    df = pd.DataFrame({
        'codigo_ips': np.random.choice(['IPS001', 'IPS002', 'IPS003', 'IPS004'], n),
        'nombre_ips': np.random.choice(ips, n),
        'departamento': np.random.choice(departamentos, n),
        'ano': np.random.choice(range(2016, 2022), n),
        'mes': np.random.choice(range(1, 13), n),
        'servicio': np.random.choice(servicios, n),
        'tiempo_espera_dias': np.clip(np.random.normal(4.2, 1.8, n), 0, 12),
        'pacientes': np.random.poisson(200, n),
        'fecha': pd.date_range('2016-01-01', periods=n, freq='D')
    })
    
    return df.sort_values('fecha').reset_index(drop=True)

# Cargar datos
st.title("🚑 **Dashboard Analítica - Tiempos de Espera IPS Colombia 2016-2021**")
st.markdown("**✅ Versión optimizada - 100% funcional en Streamlit Cloud**")

df = load_demo_data()
st.success(f"✅ Datos cargados: **{len(df):,}** registros | **{df['departamento'].nunique()}** departamentos")

# Sidebar consultas
st.sidebar.header("🔍 **Consultas Bootcamp**")
consulta = st.sidebar.selectbox("Tipo de análisis:", 
    ["📊 Overview General", "🔢 KPIs Servicios", "📈 Análisis Temporal", 
     "🏆 Ranking IPS", "🗺️ Heatmap Departamentos"])

# KPIs principales
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("📊 Registros", f"{len(df):,}")
with col2: st.metric("⏱️ Promedio", f"{df['tiempo_espera_dias'].mean():.1f} días")
with col3: st.metric("🔴 Máximo", f"{df['tiempo_espera_dias'].max():.1f} días")
with col4: st.metric("🏥 Servicios", f"{df['servicio'].nunique()}")

st.markdown("---")

# CONSULTAS BOOTCAMP OPTIMIZADAS
if consulta == "📊 Overview General":
    col1, col2 = st.columns(2)
    with col1:
        desc = df[['tiempo_espera_dias']].describe().round(2).T
        st.dataframe(desc, use_container_width=True)
    with col2:
        fig = px.pie(df, names='servicio', title="Distribución Servicios")
        st.plotly_chart(fig, use_container_width=True)

elif consulta == "🔢 KPIs Servicios":
    kpis = df.groupby('servicio')['tiempo_espera_dias'].agg([
        ('N', 'count'), ('Media', 'mean'), ('Mediana', 'median'), 
        ('Std', 'std')
    ]).round(2)
    st.dataframe(kpis, use_container_width=True)
    
    fig = px.bar(kpis.reset_index(), x='servicio', y='Media', 
                title="Promedio por Servicio")
    st.plotly_chart(fig)

elif consulta == "📈 Análisis Temporal":
    monthly = df.set_index('fecha').resample('M')['tiempo_espera_dias'].mean()
    fig = px.line(monthly.reset_index(), x='fecha', y='tiempo_espera_dias',
                 title="Evolución Mensual")
    st.plotly_chart(fig)

elif consulta == "🏆 Ranking IPS":
    ranking = df.groupby('nombre_ips')['tiempo_espera_dias'].mean().sort_values()
    fig = px.bar(ranking.reset_index(), x='tiempo_espera_dias', 
                y='nombre_ips', orientation='h',
                title="Ranking IPS (Más eficiente → Menos eficiente)")
    st.plotly_chart(fig)

elif consulta == "🗺️ Heatmap Departamentos":
    heatmap = df.pivot_table(values='tiempo_espera_dias', 
                           index='departamento', columns='ano', aggfunc='mean')
    fig = px.imshow(heatmap.round(2), title="Heatmap Dept/Año", 
                   color_continuous_scale='RdYlGn_r')
    st.plotly_chart(fig)

# Filtros + Descarga
st.sidebar.header("⚙️ Filtros")
dept = st.sidebar.multiselect("Departamento", df['departamento'].unique())
serv = st.sidebar.multiselect("Servicio", df['servicio'].unique())

df_filt = df
if dept: df_filt = df_filt[df_filt['departamento'].isin(dept)]
if serv: df_filt = df_filt[df_filt['servicio'].isin(serv)]

with st.expander("📋 Datos filtrados"):
    st.dataframe(df_filt.head(100))

# DESCARGA
csv = df_filt.to_csv(index=False).encode('utf-8')
st.download_button("💾 Descargar CSV", csv, "ips_colombia.csv", "text/csv")

st.markdown("---")
st.markdown("""
*🎓 Bootcamp Analítica Integrador | ✅ 100% Compatible Streamlit Cloud*
""")
