# scripts/converter_codigos_bairros.py
import pandas as pd
import requests
from pathlib import Path

print("= CONVERSÃO DE CÓDIGOS DE BAIRROS =\n")

# 1. Baixar mapeamento oficial
print("1. Baixando mapeamento oficial de bairros do Recife...")
url = "https://dados.recife.pe.gov.br/dataset/area-urbana/resource/5c67ce14-1799-40c4-a37c-9daa04d1761c/download/bairros-do-recife.geojson"

try:
    response = requests.get(url)
    data = response.json()
    
    bairros_list = []
    for feature in data['features']:
        props = feature['properties']
        bairros_list.append({
            'codigo_oficial': props['CBAIRRCODI'],
            'nome': props['EBAIRRNOMEOF']
        })
    
    df_bairros = pd.DataFrame(bairros_list).sort_values('nome').reset_index(drop=True)
    df_bairros['codigo_sequencial'] = df_bairros.index + 1
    
    # Salvar mapeamento
    Path('data/processed').mkdir(parents=True, exist_ok=True)
    df_bairros.to_csv('data/processed/mapeamento_bairros_oficial.csv', index=False)
    
    print(f" {len(df_bairros)} bairros baixados e mapeados")
    
except Exception as e:
    print(f" Erro ao baixar dados: {e}")
    exit(1)

# 2. Criar dicionário de conversão (código sequencial → nome)
mapeamento = dict(zip(
    df_bairros['codigo_sequencial'].astype(str), 
    df_bairros['nome']
))

print(f"\n2. Carregando dados de casos por bairro...")

# 3. Carregar arquivo de casos
try:
    df_casos = pd.read_csv('data/processed/casos_por_bairro.csv')
    print(f" {len(df_casos)} registros carregados")
except FileNotFoundError:
    print(" Arquivo 'data/processed/casos_por_bairro.csv' não encontrado!")
    print("Execute primeiro o script de consolidação de dados.")
    exit(1)

# 4. Converter códigos para nomes
print("\n3. Convertendo códigos para nomes...")
df_casos['BAIRRO'] = df_casos['BAIRRO'].astype(str).str.replace('.0', '', regex=False)
df_casos['BAIRRO_NOME'] = df_casos['BAIRRO'].map(mapeamento)

# 5. Estatísticas
total = len(df_casos)
convertidos = df_casos['BAIRRO_NOME'].notna().sum()
nao_convertidos = df_casos['BAIRRO_NOME'].isna().sum()


print(f"Total de registros: {total}")
print(f" Convertidos: {convertidos} ({convertidos/total*100:.1f}%)")
print(f" Não convertidos: {nao_convertidos} ({nao_convertidos/total*100:.1f}%)")

if nao_convertidos > 0:
    print("\nCódigos não convertidos:")
    print(df_casos[df_casos['BAIRRO_NOME'].isna()]['BAIRRO'].value_counts())

# 6. Salvar arquivo completo
df_casos.to_csv('data/processed/casos_por_bairro_com_nomes.csv', index=False)
print(f"\n Arquivo salvo: data/processed/casos_por_bairro_com_nomes.csv")

# 7. Gerar arquivo final limpo
df_final = df_casos[df_casos['BAIRRO_NOME'].notna()].copy()
df_final = df_final[['ANO', 'SEMANA', 'BAIRRO_NOME', 'CASOS']]
df_final.rename(columns={'BAIRRO_NOME': 'BAIRRO'}, inplace=True)

df_final.to_csv('data/processed/casos_dengue_bairros_2020_2025.csv', index=False)
print(f" Arquivo final limpo: data/processed/casos_dengue_bairros_2020_2025.csv")

# 8. Resumo

print("RESUMO FINAL:")
print(f"Período: {df_final['ANO'].min()} - {df_final['ANO'].max()}")
print(f"Total de registros: {len(df_final)}")
print(f"Bairros únicos: {df_final['BAIRRO'].nunique()}")

print("\nTop 10 bairros com mais casos:")
top_bairros = df_final.groupby('BAIRRO')['CASOS'].sum().sort_values(ascending=False).head(10)
for bairro, casos in top_bairros.items():
    print(f"  {bairro}: {casos} casos")


print(" Conversão concluída com sucesso!")