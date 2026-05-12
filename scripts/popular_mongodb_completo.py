import pandas as pd
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from api.database import get_database

print("Populando MongoDB com dados completos...")

# 1. Carregar dados consolidados de dengue
df_dengue = pd.read_csv("data/processed/dengue_consolidado_2019_2025.csv")
print(f"Casos de dengue: {len(df_dengue)} registros")
print(f"Período: {df_dengue['ANO'].min()} - {df_dengue['ANO'].max()}")

# 2. Carregar dados climáticos
df_clima = pd.read_csv("data/raw/dados_clima_inmet_recife.csv")
print(f"\nDados climáticos: {len(df_clima)} registros")

# 3. Processar dados climáticos
df_clima['DATA'] = pd.to_datetime(df_clima['Data'])
df_clima['ANO'] = df_clima['DATA'].dt.year
df_clima['SEMANA'] = df_clima['DATA'].dt.isocalendar().week

# Renomear colunas
df_clima['TEMP_MEDIA'] = pd.to_numeric(df_clima['TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)'], errors='coerce')
df_clima['PRECIPITACAO'] = pd.to_numeric(df_clima['PRECIPITAÇÃO TOTAL, HORÁRIO (mm)'], errors='coerce')
df_clima['UMIDADE'] = pd.to_numeric(df_clima['UMIDADE RELATIVA DO AR, HORARIA (%)'], errors='coerce')

# Agregar por semana
clima_semanal = df_clima.groupby(['ANO', 'SEMANA']).agg({
    'TEMP_MEDIA': 'mean',
    'PRECIPITACAO': 'sum',
    'UMIDADE': 'mean'
}).reset_index()

clima_semanal.columns = ['ANO', 'SEMANA', 'TEMP_MEDIA_C', 'PRECIPITACAO_MM', 'UMIDADE_MEDIA']

print(f"\nDados climáticos agregados: {len(clima_semanal)} semanas")

# 4. Merge com casos de dengue
df_completo = df_dengue.merge(clima_semanal, on=['ANO', 'SEMANA'], how='left')

# Preencher valores nulos com médias
df_completo['TEMP_MEDIA_C'] = df_completo['TEMP_MEDIA_C'].fillna(df_completo['TEMP_MEDIA_C'].mean())
df_completo['PRECIPITACAO_MM'] = df_completo['PRECIPITACAO_MM'].fillna(0)
df_completo['UMIDADE_MEDIA'] = df_completo['UMIDADE_MEDIA'].fillna(df_completo['UMIDADE_MEDIA'].mean())

print(f"\nDados integrados: {len(df_completo)} registros")
print(f"\nColunas: {list(df_completo.columns)}")
print(f"\nAmostra dos dados integrados:")
print(df_completo.head(10))

# 5. Inserir no MongoDB
db = get_database()

# Limpar collection antiga
resultado_delete = db.casos_dengue.delete_many({})
print(f"\n{resultado_delete.deleted_count} registros antigos removidos!")

# Inserir dados novos
registros = df_completo.to_dict('records')
resultado_insert = db.casos_dengue.insert_many(registros)

print(f"\n✓ {len(resultado_insert.inserted_ids)} registros inseridos no MongoDB!")
print(f"✓ Database pronto para o dashboard!")