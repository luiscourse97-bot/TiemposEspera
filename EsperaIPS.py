import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="🚑 IPS Colombia", layout="wide")

st.title("🚑 Dashboard Tiempos Espera IPS Colombia")
st.markdown("**✅ Deploy exitoso - Bootcamp Analítica**")

# DATOS DEMO MINIMALISTAS
@st.cache_data
def load_data():
    np.random.seed(42)
    n = 2000
    df = pd.DataFrame({
        'ips': [f'IPS_{i:03d}' for i in range(n)],
        'departamento': np.random.choice(['BOGOTÁ', 'ANTIOQUIA', 'VALLE'], n),
        'servicio': np.random.choice(['Medicina', 'Odontología', 'Urgencias'], n),
        'ano': np.random.choice([2016,2017,2018,2019,2020,2021], n),
        'espera_dias': np.clip(np.random.normal(3.5, 1.5, n), 0, 10)
    })
    return df

df = load_data()

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Registros", len(df))
col2.metric("Promedio", f"{df['espera_dias'].mean():.1f} días")
col3.metric("Máximo", f"{df['espera_dias'].max():.1f} días")

# Sidebar
st.sidebar.header("🔍 Análisis")
consulta = st.sidebar.selectbox("Consulta:", ["Overview", "Servicios", "Tiempo", "Ranking"])

if consulta == "Overview":
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(df.describe())
    with col2:
        fig = px.pie(df, names='servicio')
        st.plotly_chart(fig)

elif consulta == "Servicios":
    kpi = df.groupby('servicio')['espera_dias'].mean().reset_index()
    fig = px.bar(kpi, x='servicio', y='espera_dias')
    st.plotly_chart(fig)
    st.dataframe(kpi)

elif consulta == "Tiempo":
    tiempo = df.groupby('ano')['espera_dias'].mean().reset_index()
    fig = px.line(tiempo, x='ano', y='espera_dias')
    st.plotly_chart(fig)

elif consulta == "Ranking":
    ranking = df.groupby('ips')['espera_dias'].mean().sort_values().head(10)
    fig = px.bar(x=ranking.index, y=ranking.values, orientation='h')
    st.plotly_chart(fig)

# Descarga
st.sidebar.download_button("CSV", df.to_csv(index=False), "datos.csv")
