import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from pathlib import Path

print("DOWNLOAD DE DADOS CLIMATICOS - INMET\n")

Path('data/raw').mkdir(parents=True, exist_ok=True)
Path('data/processed').mkdir(parents=True, exist_ok=True)

ESTACAO_RECIFE = "A301"
anos = [2020, 2021, 2022, 2023, 2024, 2025]

print(f"Estacao: {ESTACAO_RECIFE} (Recife - PE)")
print(f"Anos: {anos[0]} a {anos[-1]}\n")

dados_clima = []

for ano in anos:
    url = f"https://portal.inmet.gov.br/uploads/dadoshistoricos/{ano}.zip"
    print(f"Baixando {ano}... ", end='')

    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            arquivo_zip = f'data/raw/clima_{ano}.zip'
            with open(arquivo_zip, 'wb') as f:
                f.write(response.content)
            print(f"OK ({len(response.content)/1024:.1f} KB)")
        else:
            print(f"ERRO (status {response.status_code})")
    except Exception as e:
        print(f"ERRO ({str(e)[:50]})")

print("\nExtracao e processamento concluidos")
print("\nNOTA: Este script baixa os arquivos ZIP.")
print("Voce precisa extrair manualmente e processar os CSVs da estacao A301.")
print("\nProximo passo: consolidar os dados climaticos de Recife em:")
print("data/processed/dados_clima_recife_apenas.csv")
