import pandas as pd

df = pd.read_csv('data/processed/casos_por_bairro_com_nomes.csv')

df_final = df[['ANO', 'SEMANA', 'BAIRRO_NOME', 'CASOS']].copy()
df_final.rename(columns={'BAIRRO_NOME': 'BAIRRO'}, inplace=True)

df_final.to_csv('data/processed/casos_dengue_bairros_2020_2025.csv', index=False)

print("✅ Dataset final pronto!")
print(f"📁 Arquivo: data/processed/casos_dengue_bairros_2020_2025.csv")
print(f"📊 Registros: {len(df_final)}")
print(f"📅 Período: 2020-2025")
print(f"🏘️ Bairros: {df_final['BAIRRO'].nunique()}")