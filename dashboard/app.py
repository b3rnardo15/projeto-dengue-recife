import streamlit as st
import sys
from pathlib import Path

# Adicionar pasta raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

from dashboard.utils.data_loader import carregar_historico, carregar_predicoes
from dashboard.components.graficos import (
    grafico_casos_tempo, 
    grafico_casos_por_ano,
    grafico_casos_vs_clima,
    grafico_sazonalidade
)

# Configuração da página
st.set_page_config(
    page_title="Dashboard Dengue Recife",
    page_icon="🦟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🦟 Sistema de Predição de Dengue - Recife")
st.markdown("---")

# Sidebar
st.sidebar.title("Navegação")
st.sidebar.markdown("""
Este dashboard apresenta análises e predições de casos de dengue em Recife 
utilizando Machine Learning e dados climáticos.
""")

# Carregar dados
with st.spinner("Carregando dados..."):
    df_historico = carregar_historico(limite=200)
    df_predicoes = carregar_predicoes(limite=50)

# Verificar se há dados
if df_historico.empty:
    st.error("⚠️ Não foi possível carregar os dados históricos. Verifique se a API está rodando.")
    st.stop()

# Métricas principais
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_casos = df_historico['CASOS'].sum()
    st.metric("Total de Casos", f"{total_casos:,.0f}")

with col2:
    media_casos = df_historico['CASOS'].mean()
    st.metric("Média Semanal", f"{media_casos:.1f}")

with col3:
    max_casos = df_historico['CASOS'].max()
    st.metric("Pico de Casos", f"{max_casos:.0f}")

with col4:
    total_predicoes = len(df_predicoes)
    st.metric("Predições Realizadas", total_predicoes)

st.markdown("---")

# Gráficos principais
st.subheader("📈 Evolução Temporal")
fig_tempo = grafico_casos_tempo(df_historico)
st.plotly_chart(fig_tempo, use_container_width=True)

# Duas colunas para gráficos
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Casos por Ano")
    fig_ano = grafico_casos_por_ano(df_historico)
    st.plotly_chart(fig_ano, use_container_width=True)

with col2:
    st.subheader("🌡️ Sazonalidade")
    fig_sazonalidade = grafico_sazonalidade(df_historico)
    st.plotly_chart(fig_sazonalidade, use_container_width=True)

# Análise climática
st.markdown("---")
st.subheader("🌦️ Relação com Variáveis Climáticas")

variavel_clima = st.selectbox(
    "Selecione a variável climática:",
    ["TEMP_MEDIA_C", "PRECIPITACAO_MM", "UMIDADE_MEDIA"],
    format_func=lambda x: {
        "TEMP_MEDIA_C": "Temperatura Média",
        "PRECIPITACAO_MM": "Precipitação",
        "UMIDADE_MEDIA": "Umidade Relativa"
    }[x]
)

fig_clima = grafico_casos_vs_clima(df_historico, variavel_clima)
st.plotly_chart(fig_clima, use_container_width=True)

# Rodapé
st.markdown("---")
st.markdown("""
**Fonte dos dados:** Portal de Dados Abertos da Prefeitura do Recife | INMET  
**Modelo:** Ridge Regression (MAE: 10.86, R²: 0.629)  
**Desenvolvido por:** BioLens
""")