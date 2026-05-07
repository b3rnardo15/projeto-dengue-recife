import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')


print("SCRIPT 1: CONSOLIDAÇÃO DOS DADOS DE DENGUE (2019-2025)")


arquivos_dengue = [
    'casos-de-dengue-2019.csv',
    'casos-de-dengue-2020.csv',
    'casos-de-dengue-2021.csv',
    'casos-de-dengue-2022.csv',
    'casos-de-dengue-2023.csv',
    'casos-de-dengue-2024.csv',
    'casos-de-dengue-2025.csv'
]

df_consolidado = pd.DataFrame()

for arquivo in arquivos_dengue:
    try:
        df_temp = pd.read_csv(arquivo, sep=';', encoding='utf-8', low_memory=False)
        df_temp['ANO_ARQUIVO'] = arquivo.replace('casos-de-dengue-', '').replace('.csv', '')
        df_consolidado = pd.concat([df_consolidado, df_temp], ignore_index=True)
        print(f"✓ {arquivo}: {len(df_temp):,} registros carregados")
    except Exception as e:
        print(f"✗ Erro ao carregar {arquivo}: {str(e)}")


print(f"TOTAL DE REGISTROS CONSOLIDADOS: {len(df_consolidado):,}")


colunas_essenciais = [
    'NU_NOTIFIC', 'DT_NOTIFIC', 'DT_SIN_PRI', 'SEM_NOT', 'SEM_PRI', 'NU_ANO',
    'ID_BAIRRO', 'NM_BAIRRO', 'ID_DISTRIT', 'CS_SEXO', 'NU_IDADE_N',
    'CLASSI_FIN', 'CRITERIO', 'EVOLUCAO', 'HOSPITALIZ', 'ANO_ARQUIVO'
]

df_dengue_limpo = df_consolidado[colunas_essenciais].copy()

df_dengue_limpo['DT_NOTIFIC'] = pd.to_datetime(df_dengue_limpo['DT_NOTIFIC'], format='%d/%m/%Y', errors='coerce')
df_dengue_limpo['DT_SIN_PRI'] = pd.to_datetime(df_dengue_limpo['DT_SIN_PRI'], format='%d/%m/%Y', errors='coerce')

df_dengue_limpo = df_dengue_limpo.sort_values('DT_NOTIFIC').reset_index(drop=True)

df_dengue_limpo.to_csv('dengue_consolidado_2019_2025.csv', index=False, encoding='utf-8')
print("\n✓ Arquivo salvo: dengue_consolidado_2019_2025.csv")


print("RESUMO ESTATÍSTICO:")

print(f"\nPeríodo: {df_dengue_limpo['DT_NOTIFIC'].min()} até {df_dengue_limpo['DT_NOTIFIC'].max()}")
print(f"\nDistribuição por ano:")
print(df_dengue_limpo.groupby('ANO_ARQUIVO').size())
print(f"\nCasos confirmados (CLASSI_FIN = 10): {len(df_dengue_limpo[df_dengue_limpo['CLASSI_FIN'] == 10]):,}")