import pandas as pd
from pathlib import Path
import requests

print("Processando dados COM conversão de códigos de bairros (V3 - CORRIGIDO)...")

print("\n1. Obtendo mapeamento oficial de bairros...")
url = "https://dados.recife.pe.gov.br/dataset/area-urbana/resource/5c67ce14-1799-40c4-a37c-9daa04d1761c/download/bairros-do-recife.geojson"
response = requests.get(url)
data = response.json()

bairros_list = []
for feature in data['features']:
    props = feature['properties']
    bairros_list.append({'codigo': props['CBAIRRCODI'], 'nome': props['EBAIRRNOMEOF']})

df_bairros = pd.DataFrame(bairros_list).sort_values('nome').reset_index(drop=True)
df_bairros['codigo_sequencial'] = df_bairros.index + 1
mapeamento = dict(zip(df_bairros['codigo_sequencial'].astype(str), df_bairros['nome']))

print(f"✓ {len(mapeamento)} bairros mapeados")

data_raw = Path("data/raw")
anos = [2019, 2020, 2021, 2022, 2023, 2024, 2025]
casos_totais = []

for ano in anos:
    arquivo = data_raw / f"casos-de-dengue-{ano}.csv"
    if not arquivo.exists():
        continue

    print(f"\n2. Processando {ano}...")
    df = pd.read_csv(arquivo, encoding='latin1', sep=';', low_memory=False)

    col_municipio = col_bairro = col_data = None

    for col in df.columns:
        col_lower = str(col).lower()
        if any(x in col_lower for x in ['co_municipio_residencia', 'id_municip', 'id_mn_resi']):
            col_municipio = col
        if 'co_bairro_residencia' in col_lower:  # FORÇA usar código, não nome
            col_bairro = col
        if any(x in col_lower for x in ['dt_notific', 'dt_sin_pri']):
            col_data = col

    if not all([col_municipio, col_data, col_bairro]):
        print(f"  ⚠️ Coluna faltando - municipio:{col_municipio}, bairro:{col_bairro}, data:{col_data}")
        continue

    df[col_municipio] = pd.to_numeric(df[col_municipio], errors='coerce')
    df_recife = df[df[col_municipio] == 261160].copy()

    if len(df_recife) == 0:
        continue

    df_recife['DATA'] = pd.to_datetime(df_recife[col_data], errors='coerce')
    df_recife = df_recife.dropna(subset=['DATA'])
    df_recife['ANO'] = df_recife['DATA'].dt.year
    df_recife['SEMANA'] = df_recife['DATA'].dt.isocalendar().week

    df_recife['BAIRRO_COD'] = df_recife[col_bairro].astype(str).str.replace('.0', '', regex=False)
    df_recife['BAIRRO'] = df_recife['BAIRRO_COD'].map(mapeamento)

    casos_totais.append(df_recife[['ANO', 'SEMANA', 'BAIRRO']])
    print(f"  ✓ {len(df_recife)} casos processados")

df_completo = pd.concat(casos_totais, ignore_index=True)
print(f"\nAntes de filtrar: {len(df_completo)}")
print(f"Com bairro válido: {df_completo['BAIRRO'].notna().sum()}")
print(f"Sem bairro: {df_completo['BAIRRO'].isna().sum()}")

df_completo = df_completo[df_completo['BAIRRO'].notna()]

casos_por_bairro = df_completo.groupby(['ANO', 'SEMANA', 'BAIRRO']).size().reset_index(name='CASOS')

print(f"\n{'='*60}")
print(f"Total: {len(casos_por_bairro)} registros")
print(f"\nTop 10 bairros:")
print(df_completo.groupby('BAIRRO').size().sort_values(ascending=False).head(10))

casos_por_bairro.to_csv('data/processed/casos_dengue_por_bairro_final.csv', index=False)
print("\n✓ Salvo: data/processed/casos_dengue_por_bairro_final.csv")