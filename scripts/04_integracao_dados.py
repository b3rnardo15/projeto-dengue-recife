import pandas as pd
from pathlib import Path

print("INTEGRACAO DE DADOS - DENGUE + CLIMA")


print("\nCarregando dados de dengue...")
df_dengue = pd.read_csv('data/processed/dengue_consolidado_2019_2025.csv')
print(f"  -> {len(df_dengue)} semanas carregadas")

print("\nCarregando dados de clima...")
df_clima = pd.read_csv('data/raw/dados_clima_inmet_recife.csv')

df_clima['DATA_HORA'] = pd.to_datetime(
    df_clima['Data'] + ' ' + df_clima['Hora UTC'].str.replace(' UTC', ''),
    format='%Y/%m/%d %H%M',
    errors='coerce'
)
df_clima = df_clima.dropna(subset=['DATA_HORA'])

df_clima['ANO'] = df_clima['DATA_HORA'].dt.year
df_clima['SEMANA'] = df_clima['DATA_HORA'].dt.isocalendar().week

clima_semanal = df_clima.groupby(['ANO', 'SEMANA']).agg({
    'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)': 'sum',
    'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)': 'mean',
    'UMIDADE RELATIVA DO AR, HORARIA (%)': 'mean'
}).reset_index()

clima_semanal.columns = ['ANO', 'SEMANA', 'PRECIPITACAO_MM', 'TEMP_MEDIA_C', 'UMIDADE_MEDIA']
print(f"  -> {len(clima_semanal)} semanas processadas")

print("\nIntegrando datasets...")
df_final = pd.merge(df_dengue, clima_semanal, on=['ANO', 'SEMANA'], how='inner')
df_final = df_final.dropna()

output_path = Path('data/processed')
output_file = output_path / 'dados_integrados_dengue_clima.csv'
df_final.to_csv(output_file, index=False)

print(f"\nArquivo salvo: {output_file}")
print(f"Total de registros integrados: {len(df_final)}")
print(f"\nColunas finais: {list(df_final.columns)}")
print(f"\nPreview:")
print(df_final.head(10))
print("\nIntegracao concluida!")