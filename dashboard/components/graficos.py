import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def grafico_casos_tempo(df: pd.DataFrame) -> go.Figure:
    """Gráfico de linha: casos ao longo do tempo"""
    if df.empty:
        return go.Figure()
    
    df['DATA'] = pd.to_datetime(df['ANO'].astype(str) + '-W' + df['SEMANA'].astype(str) + '-1', format='%Y-W%W-%w')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['DATA'],
        y=df['CASOS'],
        mode='lines+markers',
        name='Casos Confirmados',
        line=dict(color='#FF6B6B', width=2),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title='Evolução de Casos de Dengue em Recife (2021-2025)',
        xaxis_title='Data',
        yaxis_title='Número de Casos',
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig

def grafico_casos_por_ano(df: pd.DataFrame) -> go.Figure:
    """Gráfico de barras: casos por ano"""
    if df.empty:
        return go.Figure()
    
    casos_ano = df.groupby('ANO')['CASOS'].sum().reset_index()
    
    fig = px.bar(
        casos_ano,
        x='ANO',
        y='CASOS',
        title='Total de Casos por Ano',
        labels={'CASOS': 'Total de Casos', 'ANO': 'Ano'},
        color='CASOS',
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(
        template='plotly_white',
        height=400
    )
    
    return fig

def grafico_casos_vs_clima(df: pd.DataFrame, variavel: str) -> go.Figure:
    """Gráfico de dispersão: casos vs variável climática"""
    if df.empty or variavel not in df.columns:
        return go.Figure()
    
    labels = {
        'TEMP_MEDIA_C': 'Temperatura Média (°C)',
        'PRECIPITACAO_MM': 'Precipitação (mm)',
        'UMIDADE_MEDIA': 'Umidade Relativa (%)'
    }
    
    fig = px.scatter(
        df,
        x=variavel,
        y='CASOS',
        title=f'Casos de Dengue vs {labels.get(variavel, variavel)}',
        labels={'CASOS': 'Casos', variavel: labels.get(variavel, variavel)},
        trendline='ols',
        color='CASOS',
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(
        template='plotly_white',
        height=400
    )
    
    return fig

def grafico_sazonalidade(df: pd.DataFrame) -> go.Figure:
    """Gráfico de sazonalidade: casos por semana do ano"""
    if df.empty:
        return go.Figure()
    
    sazonalidade = df.groupby('SEMANA')['CASOS'].mean().reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=sazonalidade['SEMANA'],
        y=sazonalidade['CASOS'],
        name='Média de Casos',
        marker_color='#FF6B6B'
    ))
    
    fig.update_layout(
        title='Sazonalidade: Média de Casos por Semana do Ano',
        xaxis_title='Semana do Ano',
        yaxis_title='Média de Casos',
        template='plotly_white',
        height=400
    )
    
    return fig

def grafico_predicoes(df_historico: pd.DataFrame, df_predicoes: pd.DataFrame) -> go.Figure:
    """Gráfico comparando casos reais vs preditos"""
    fig = go.Figure()
    
    if not df_historico.empty:
        df_historico['DATA'] = pd.to_datetime(
            df_historico['ANO'].astype(str) + '-W' + df_historico['SEMANA'].astype(str) + '-1', 
            format='%Y-W%W-%w'
        )
        fig.add_trace(go.Scatter(
            x=df_historico['DATA'],
            y=df_historico['CASOS'],
            mode='lines',
            name='Casos Reais',
            line=dict(color='#4ECDC4', width=2)
        ))
    
    if not df_predicoes.empty:
        df_predicoes['DATA'] = pd.to_datetime(
            df_predicoes['ano'].astype(str) + '-W' + df_predicoes['semana'].astype(str) + '-1',
            format='%Y-W%W-%w'
        )
        fig.add_trace(go.Scatter(
            x=df_predicoes['DATA'],
            y=df_predicoes['casos_preditos'],
            mode='markers',
            name='Predições',
            marker=dict(color='#FF6B6B', size=10, symbol='diamond')
        ))
    
    fig.update_layout(
        title='Casos Reais vs Predições',
        xaxis_title='Data',
        yaxis_title='Número de Casos',
        template='plotly_white',
        hovermode='x unified',
        height=400
    )
    
    return fig