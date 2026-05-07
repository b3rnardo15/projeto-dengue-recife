import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("SCRIPT 4: INTEGRACAO DE DADOS E FEATURE ENGINEERING")


print("\n[1/6] Carregando dados de dengue...")
df_dengue = pd.read_csv('dengue_consolidado_2019_2025.csv', parse_dates=['DT_NOTIFIC', 'DT_SIN_PRI'])
df_dengue_confirmados = df_dengue[df_dengue['CLASSI_FIN'] == 10].copy()
print(f"Casos confirmados carregados: {len(df_dengue_confirmados):,}")

print("\n[2/6] Carregando dados climaticos...")
df_clima = pd.read_csv('dados_clima_recife_apenas.csv')
df_clima['Data'] = pd.to_datetime(df_clima['Data'], format='%Y/%m/%d')

def converter_para_float(coluna):
    if coluna.dtype == 'object':
        return pd.to_numeric(coluna.str.replace(',', '.'), errors='coerce')
    else:
        return pd.to_numeric(coluna, errors='coerce')

df_clima['TEMP_BULBO'] = converter_para_float(df_clima['TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)'])
df_clima['PRECIPITACAO'] = converter_para_float(df_clima['PRECIPITAÇÃO TOTAL, HORÁRIO (mm)'])
df_clima['UMIDADE'] = converter_para_float(df_clima['UMIDADE RELATIVA DO AR, HORARIA (%)'])

print(f"Registros climaticos carregados: {len(df_clima):,}")

print("\n[3/6] Agregando dados climaticos por dia...")
df_clima_diario = df_clima.groupby('Data').agg({
    'TEMP_BULBO': ['mean', 'max', 'min'],
    'PRECIPITACAO': 'sum',
    'UMIDADE': 'mean'
}).reset_index()

df_clima_diario.columns = ['DATA', 'TEMP_MEDIA', 'TEMP_MAX', 'TEMP_MIN', 'PRECIPITACAO_TOTAL', 'UMIDADE_MEDIA']
print(f"Agregado em dias: {len(df_clima_diario):,}")

print("\n[4/6] Agregando casos de dengue por dia...")
df_dengue_diario = df_dengue_confirmados.groupby(df_dengue_confirmados['DT_NOTIFIC'].dt.date).size().reset_index()
df_dengue_diario.columns = ['DATA', 'CASOS']
df_dengue_diario['DATA'] = pd.to_datetime(df_dengue_diario['DATA'])
print(f"Dias com casos: {len(df_dengue_diario):,}")

print("\n[5/6] Integrando dados de dengue e clima...")
df_integrado = pd.merge(df_clima_diario, df_dengue_diario, on='DATA', how='left')
df_integrado['CASOS'] = df_integrado['CASOS'].fillna(0)

df_integrado['ANO'] = df_integrado['DATA'].dt.year
df_integrado['MES'] = df_integrado['DATA'].dt.month
df_integrado['SEMANA'] = df_integrado['DATA'].dt.isocalendar().week
df_integrado['DIA_ANO'] = df_integrado['DATA'].dt.dayofyear

print(f"Dataset integrado: {len(df_integrado):,} registros")

print("\n[6/6] Criando features para modelagem...")
df_integrado = df_integrado.sort_values('DATA').reset_index(drop=True)

for lag in [7, 14, 21, 30]:
    df_integrado[f'CASOS_LAG_{lag}'] = df_integrado['CASOS'].shift(lag)
    df_integrado[f'TEMP_LAG_{lag}'] = df_integrado['TEMP_MEDIA'].shift(lag)
    df_integrado[f'PRECIP_LAG_{lag}'] = df_integrado['PRECIPITACAO_TOTAL'].shift(lag)

df_integrado['CASOS_MA_7'] = df_integrado['CASOS'].rolling(window=7).mean()
df_integrado['CASOS_MA_14'] = df_integrado['CASOS'].rolling(window=14).mean()
df_integrado['CASOS_MA_30'] = df_integrado['CASOS'].rolling(window=30).mean()

df_integrado['TEMP_MA_7'] = df_integrado['TEMP_MEDIA'].rolling(window=7).mean()
df_integrado['PRECIP_MA_7'] = df_integrado['PRECIPITACAO_TOTAL'].rolling(window=7).mean()

df_integrado = df_integrado.dropna()

print(f"Dataset final com features: {len(df_integrado):,} registros")
print(f"Total de features: {len(df_integrado.columns)}")

df_integrado.to_csv('dataset_dengue_clima_integrado.csv', index=False)
print("\nArquivo salvo: dataset_dengue_clima_integrado.csv")


print("ANALISE DE CORRELACAO")


colunas_analise = ['CASOS', 'TEMP_MEDIA', 'TEMP_MAX', 'TEMP_MIN', 'PRECIPITACAO_TOTAL', 'UMIDADE_MEDIA']
correlacao = df_integrado[colunas_analise].corr()

print("\nCorrelacao com CASOS de dengue:")
print(correlacao['CASOS'].sort_values(ascending=False))

plt.figure(figsize=(12, 8))
sns.heatmap(correlacao, annot=True, cmap='coolwarm', center=0, fmt='.2f')
plt.title('Matriz de Correlacao: Dengue vs Variaveis Climaticas')
plt.tight_layout()
plt.savefig('correlacao_dengue_clima.png', dpi=150)
print("\nGrafico salvo: correlacao_dengue_clima.png")


print("ESTATISTICAS DESCRITIVAS")

print(df_integrado[colunas_analise].describe())

print("INTEGRACAO CONCLUIDA")
