import pandas as pd

df = pd.read_csv('data/raw/dados_clima_inmet_recife.csv', nrows=5)
print("Colunas do arquivo:")
print(list(df.columns))
print("\nPrimeiras linhas:")
print(df.head())