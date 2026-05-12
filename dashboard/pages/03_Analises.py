import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import plotly.express as px

sys.path.append(str(Path(__file__).parent.parent.parent))

from dashboard.utils.data_loader import carregar_historico
from dashboard.components.graficos import grafico_casos_vs_clima

st.set_page_config(page_title="Análises", page_icon="📉", layout="wide")

st.title("📉 Análises Avançadas")
st.markdown("Correlações, tendências e insights dos dados")
st.markdown("---")

# Carregar dados
df = carregar_historico(limite=200)

if df.empty:
    st.error("⚠️ Não foi possível carregar os dados.")
    st.stop()

# Análise de correlação
st.subheader("🔗 Matriz de Correlação")

# Selecionar apenas colunas numéricas
colunas_numericas = ['CASOS', 'TEMP_MEDIA_C', 'PRECIPITACAO_MM', 'UMIDADE_MEDIA']
df_corr = df[colunas_numericas].corr()

fig_corr = px.imshow(
    df_corr,
    text_auto='.2f',
    aspect='auto',
    color_continuous_scale='RdBu_r',
    labels=dict(x="Variável", y="Variável", color="Correlação"),
    title="Correlação entre Casos e Variáveis Climáticas"
)

st.plotly_chart(fig_corr, use_container_width=True)

# Insights
st.markdown("---")
st.subheader("💡 Insights Principais")

col1, col2 = st.columns(2)

with col1:
    corr_temp = df_corr.loc['CASOS', 'TEMP_MEDIA_C']
    st.metric("Correlação com Temperatura", f"{corr_temp:.3f}")
    
    if corr_temp > 0:
        st.info("📈 Correlação positiva: casos tendem a aumentar com temperatura")
    else:
        st.info("📉 Correlação negativa: casos tendem a diminuir com temperatura")

with col2:
    corr_precip = df_corr.loc['CASOS', 'PRECIPITACAO_MM']
    st.metric("Correlação com Precipitação", f"{corr_precip:.3f}")
    
    if corr_precip > 0:
        st.info("📈 Correlação positiva: casos tendem a aumentar com chuva")
    else:
        st.info("📉 Correlação negativa: casos tendem a diminuir com chuva")

# Análise por variável
st.markdown("---")
st.subheader("🌦️ Análise Detalhada por Variável Climática")

variavel = st.selectbox(
    "Selecione a variável:",
    ["TEMP_MEDIA_C", "PRECIPITACAO_MM", "UMIDADE_MEDIA"],
    format_func=lambda x: {
        "TEMP_MEDIA_C": "🌡️ Temperatura Média",
        "PRECIPITACAO_MM": "🌧️ Precipitação",
        "UMIDADE_MEDIA": "💧 Umidade Relativa"
    }[x]
)

fig_clima = grafico_casos_vs_clima(df, variavel)
st.plotly_chart(fig_clima, use_container_width=True)

# Estatísticas descritivas
st.markdown("---")
st.subheader("📊 Estatísticas Descritivas")

st.dataframe(df[colunas_numericas].describe().round(2), use_container_width=True)

# Informações do modelo
st.markdown("---")
st.subheader("🤖 Informações do Modelo")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Modelo", "Ridge Regression")
    st.caption("Regressão linear regularizada")

with col2:
    st.metric("MAE", "10.86 casos")
    st.caption("Erro médio absoluto")

with col3:
    st.metric("R² Score", "0.629")
    st.caption("Coeficiente de determinação")

st.info("""
**Features utilizadas:** 16 variáveis incluindo lags temporais (7, 14, 21, 30 dias), 
médias móveis, temperatura, precipitação, umidade e features temporais (mês, semana).
""")