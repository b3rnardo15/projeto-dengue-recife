import pandas as pd
from pathlib import Path

print("CONSOLIDACAO DE DADOS DE DENGUE - RECIFE")

raw_path = Path('data/raw')
processed_path = Path('data/processed')
processed_path.mkdir(parents=True, exist_ok=True)

anos = [2019, 2020, 2021, 2022, 2023, 2024, 2025]
dfs = []

for ano in anos:
    arquivo = raw_path / f'casos-de-dengue-{ano}.csv'
    
    if not arquivo.exists():
        print(f"AVISO: Arquivo {arquivo} nao encontrado. Pulando...")
        continue
    
    print(f"Lendo {arquivo.name}...")
    
    df_ano = pd.read_csv(
        arquivo, 
        sep=';',
        encoding='latin1',
        low_memory=False,
        on_bad_lines='skip'
    )
    
    if 'DT_NOTIFIC' not in df_ano.columns:
        print(f"  ERRO: Coluna DT_NOTIFIC nao encontrada!")
        continue
    
    df_ano['DATA'] = pd.to_datetime(df_ano['DT_NOTIFIC'], format='%d/%m/%Y', errors='coerce')
    df_ano = df_ano.dropna(subset=['DATA'])
    
    df_ano['ANO'] = df_ano['DATA'].dt.year
    df_ano['MES'] = df_ano['DATA'].dt.month
    df_ano['SEMANA'] = df_ano['DATA'].dt.isocalendar().week
    
    df_filtrado = df_ano[['DATA', 'ANO', 'MES', 'SEMANA']].copy()
    dfs.append(df_filtrado)
    print(f"  -> {len(df_filtrado)} notificacoes processadas")

if not dfs:
    print("\nERRO: Nenhum arquivo processado!")
    exit(1)

df_consolidado = pd.concat(dfs, ignore_index=True)
df_consolidado = df_consolidado.sort_values('DATA').reset_index(drop=True)

casos_semana = df_consolidado.groupby(['ANO', 'SEMANA']).size().reset_index(name='CASOS')

output_file = processed_path / 'dengue_consolidado_2019_2025.csv'
casos_semana.to_csv(output_file, index=False)

print(f"\nArquivo salvo: {output_file}")
print(f"Total de registros: {len(df_consolidado)}")
print(f"Total de semanas: {len(casos_semana)}")
print(f"Periodo: {df_consolidado['DATA'].min()} a {df_consolidado['DATA'].max()}")