import streamlit as st
import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent.parent))

from dashboard.utils.data_loader import carregar_predicoes, fazer_predicao, carregar_historico
from dashboard.components.graficos import grafico_predicoes

st.set_page_config(page_title="Predições", page_icon="🔮", layout="wide")

st.title("🔮 Predições de Casos de Dengue")
st.markdown("Faça novas predições e visualize predições anteriores")
st.markdown("---")

# Tabs
tab1, tab2 = st.tabs(["Nova Predição", "Histórico de Predições"])

# Tab 1: Nova predição
with tab1:
    st.subheader("🎯 Fazer Nova Predição")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Dados Temporais:**")
        ano = st.number_input("Ano:", min_value=2026, max_value=2030, value=2026)
        semana = st.number_input("Semana:", min_value=1, max_value=53, value=1)
    
    with col2:
        st.markdown("**Dados Climáticos:**")
        temperatura = st.slider("Temperatura Média (°C):", 20.0, 35.0, 27.0, 0.5)
        precipitacao = st.slider("Precipitação (mm):", 0.0, 200.0, 50.0, 5.0)
        umidade = st.slider("Umidade Relativa (%):", 40.0, 100.0, 75.0, 1.0)
    
    st.markdown("---")
    
    if st.button("🚀 Fazer Predição", type="primary", use_container_width=True):
        with st.spinner("Processando predição..."):
            resultado = fazer_predicao(precipitacao, temperatura, umidade, ano, semana)
        
        if resultado:
            st.success("✅ Predição realizada com sucesso!")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Casos Preditos", f"{resultado['casos_preditos']:.0f}")
            
            with col2:
                st.metric("Ano/Semana", f"{resultado['ano']}/S{resultado['semana']}")
            
            with col3:
                data_pred = pd.to_datetime(resultado.get('data_predicao', datetime.now()))
                st.metric("Data da Predição", data_pred.strftime("%d/%m/%Y"))
            
            st.json(resultado)
        else:
            st.error("❌ Erro ao fazer predição. Verifique se a API está rodando.")

# Tab 2: Histórico de predições
with tab2:
    st.subheader("📜 Histórico de Predições Realizadas")
    
    limite_pred = st.slider("Quantidade de predições:", 5, 50, 20, key="limite_pred")
    
    df_predicoes = carregar_predicoes(limite=limite_pred)
    
    if df_predicoes.empty:
        st.info("ℹ️ Ainda não há predições realizadas. Faça sua primeira predição na aba acima!")
    else:
        # Métricas
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total de Predições", len(df_predicoes))
        
        with col2:
            media_pred = df_predicoes['casos_preditos'].mean()
            st.metric("Média Predita", f"{media_pred:.1f}")
        
        with col3:
            max_pred = df_predicoes['casos_preditos'].max()
            st.metric("Maior Predição", f"{max_pred:.0f}")
        
        st.markdown("---")
        
        # Gráfico comparativo
        st.subheader("📊 Comparação: Casos Reais vs Predições")
        df_historico = carregar_historico(limite=200)
        fig_comp = grafico_predicoes(df_historico, df_predicoes)
        st.plotly_chart(fig_comp, use_container_width=True)
        
        # Tabela de predições
        st.markdown("---")
        st.subheader("📋 Tabela de Predições")
        
        df_display = df_predicoes.copy()
        
        # Renomear colunas
        df_display = df_display.rename(columns={
            'ano': 'Ano',
            'semana': 'Semana',
            'casos_preditos': 'Casos Preditos',
            'temp_media_c': 'Temperatura (°C)',
            'precipitacao_mm': 'Precipitação (mm)',
            'umidade_media': 'Umidade (%)',
            'data_predicao': 'Data da Predição'
        })
        
        # Formatar data
        if 'Data da Predição' in df_display.columns:
            df_display['Data da Predição'] = pd.to_datetime(df_display['Data da Predição']).dt.strftime('%d/%m/%Y %H:%M')
        
        # Arredondar valores
        if 'Casos Preditos' in df_display.columns:
            df_display['Casos Preditos'] = df_display['Casos Preditos'].round(0)
        
        st.dataframe(df_display, use_container_width=True, height=400)
        
        # Download
        st.download_button(
            label="📥 Baixar predições em CSV",
            data=df_display.to_csv(index=False).encode('utf-8'),
            file_name='predicoes_dengue.csv',
            mime='text/csv'
        )