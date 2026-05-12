import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from dashboard.utils.data_loader import carregar_historico
from dashboard.components.graficos import (
    grafico_casos_tempo,
    grafico_casos_por_ano,
    grafico_sazonalidade
)

st.set_page_config(page_title="Histórico de Casos", page_icon="📊", layout="wide")

st.title("📊 Histórico de Casos de Dengue")
st.markdown("Análise detalhada dos casos históricos de dengue em Recife (2021-2025)")
st.markdown("---")

# Filtros
col1, col2 = st.columns([1, 3])

with col1:
    ano_selecionado = st.selectbox(
        "Filtrar por ano:",
        ["Todos"] + list(range(2021, 2026))
    )
    
    limite = st.slider("Quantidade de registros:", 10, 200, 157)

# Carregar dados
if ano_selecionado == "Todos":
    df = carregar_historico(limite=limite)
else:
    df = carregar_historico(ano=ano_selecionado, limite=limite)

if df.empty:
    st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados.")
    st.stop()

# Estatísticas
st.subheader("📈 Estatísticas Gerais")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total de Registros", len(df))

with col2:
    st.metric("Total de Casos", f"{df['CASOS'].sum():,.0f}")

with col3:
    st.metric("Média por Semana", f"{df['CASOS'].mean():.1f}")

with col4:
    st.metric("Desvio Padrão", f"{df['CASOS'].std():.1f}")

st.markdown("---")

# Gráficos
st.subheader("📈 Visualizações")

tab1, tab2, tab3 = st.tabs(["Evolução Temporal", "Por Ano", "Sazonalidade"])

with tab1:
    fig_tempo = grafico_casos_tempo(df)
    st.plotly_chart(fig_tempo, use_container_width=True)

with tab2:
    fig_ano = grafico_casos_por_ano(df)
    st.plotly_chart(fig_ano, use_container_width=True)

with tab3:
    fig_sazonalidade = grafico_sazonalidade(df)
    st.plotly_chart(fig_sazonalidade, use_container_width=True)

# Tabela de dados
st.markdown("---")
st.subheader("📋 Dados Brutos")

# Ordenar por ano e semana decrescente
df_display = df.sort_values(['ANO', 'SEMANA'], ascending=False)

# Renomear colunas para exibição
df_display = df_display.rename(columns={
    'ANO': 'Ano',
    'SEMANA': 'Semana',
    'CASOS': 'Casos',
    'TEMP_MEDIA_C': 'Temp. Média (°C)',
    'PRECIPITACAO_MM': 'Precipitação (mm)',
    'UMIDADE_MEDIA': 'Umidade (%)'
})

# Formatar valores numéricos
if 'Temp. Média (°C)' in df_display.columns:
    df_display['Temp. Média (°C)'] = df_display['Temp. Média (°C)'].round(1)
if 'Precipitação (mm)' in df_display.columns:
    df_display['Precipitação (mm)'] = df_display['Precipitação (mm)'].round(1)
if 'Umidade (%)' in df_display.columns:
    df_display['Umidade (%)'] = df_display['Umidade (%)'].round(1)

st.dataframe(df_display, use_container_width=True, height=400)

# Download
st.download_button(
    label="📥 Baixar dados em CSV",
    data=df_display.to_csv(index=False).encode('utf-8'),
    file_name=f'dengue_recife_{ano_selecionado}.csv',
    mime='text/csv'
)