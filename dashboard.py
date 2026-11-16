import os
import json
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Monitor NutriBot", layout="wide")

ARCHIVO_LOGS = "logs_observabilidad.jsonl"

st.title("Panel de Observabilidad y Trazabilidad - NutriBot")
st.caption("Evaluación Parcial N°3 | Ingeniería de Soluciones con IA (ISY0101)")

if not os.path.exists(ARCHIVO_LOGS):
    st.warning("No hay datos todavía. Corre 'python test_observabilidad.py' primero.")
    st.stop()

filas = []
with open(ARCHIVO_LOGS, "r", encoding="utf-8") as f:
    for linea in f:
        if linea.strip():
            filas.append(json.loads(linea))

df = pd.DataFrame(filas)
df["ejecucion"] = range(1, len(df) + 1)

st.sidebar.header("Filtros")
filtro_esc = st.sidebar.multiselect("Escenario", df["escenario"].unique(), default=df["escenario"].unique())
filtro_tool = st.sidebar.multiselect("Herramienta", df["herramienta"].unique(), default=df["herramienta"].unique())

df_vista = df[(df["escenario"].isin(filtro_esc)) & (df["herramienta"].isin(filtro_tool))]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Consultas analizadas", len(df_vista))
c2.metric("Latencia media", f"{df_vista['latencia_seg'].mean():.2f} s", f"Max: {df_vista['latencia_seg'].max():.2f} s")
c3.metric("Tasa de éxito", f"{(df_vista['estado'] == 'ok').mean() * 100:.0f}%")
c4.metric("RAM promedio", f"{df_vista['ram_mb'].mean():.0f} MB")
c5.metric("PII enmascarados", int(df_vista["pii_detectado"].sum()), f"Fallbacks: {int(df_vista['fallback_activado'].sum())}")

st.divider()

col_izq, col_der = st.columns(2)

with col_izq:
    st.subheader("Latencia por consulta (segundos)")
    fig1 = px.line(df_vista, x="ejecucion", y="latencia_seg", color="escenario", markers=True)
    st.plotly_chart(fig1, use_container_width=True)

with col_der:
    st.subheader("Uso de herramientas por el agente")
    conteo = df_vista["herramienta"].value_counts().reset_index()
    conteo.columns = ["Herramienta", "Total"]
    fig2 = px.pie(conteo, names="Herramienta", values="Total", hole=0.35)
    st.plotly_chart(fig2, use_container_width=True)

col_izq2, col_der2 = st.columns(2)

with col_izq2:
    st.subheader("Consumo de memoria RAM del proceso (MB)")
    fig3 = px.bar(df_vista, x="ejecucion", y="ram_mb", color="herramienta")
    st.plotly_chart(fig3, use_container_width=True)

with col_der2:
    st.subheader("Dispersión de tiempos por tipo de escenario")
    fig4 = px.box(df_vista, x="escenario", y="latencia_seg", color="escenario")
    st.plotly_chart(fig4, use_container_width=True)

st.divider()
st.subheader("Logs de trazabilidad detallados")
cols = ["ejecucion", "thread_id", "escenario", "pregunta", "herramienta", "latencia_seg", "ram_mb", "fallback_activado", "pii_detectado", "estado"]
st.dataframe(df_vista[cols], use_container_width=True)