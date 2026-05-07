import pandas as pd
import zipfile
from pathlib import Path


print("SCRIPT 2D: EXTRAÇÃO DE DADOS CLIMÁTICOS DE RECIFE")


zips_encontrados = sorted(Path('.').glob('*.zip'))

print(f"\n Encontrados {len(zips_encontrados)} arquivo(s) ZIP\n")

df_clima_recife = pd.DataFrame()

estacoes_recife = ['A301', '82900', 'RECIFE']

for zip_file in zips_encontrados:
    ano = str(zip_file).split('.')[0][-4:] if any(char.isdigit() for char in str(zip_file)) else "2025"
    
    print(f" Processando: {zip_file}")
    
    try:
        with zipfile.ZipFile(zip_file, 'r') as z:
            arquivos_csv = [f for f in z.namelist() if f.upper().endswith('.CSV')]
            
            for arquivo in arquivos_csv:
                nome_upper = arquivo.upper()
                
                if any(estacao in nome_upper for estacao in estacoes_recife):
                    try:
                        df_temp = pd.read_csv(
                            z.open(arquivo), 
                            sep=';', 
                            encoding='latin1', 
                            skiprows=8,
                            decimal=',',
                            on_bad_lines='skip'
                        )
                        
                        df_temp['ARQUIVO_ORIGEM'] = arquivo
                        df_temp['ANO_ORIGEM'] = ano
                        df_clima_recife = pd.concat([df_clima_recife, df_temp], ignore_index=True)
                        
                        print(f"   {arquivo}: {len(df_temp)} registros")
                    
                    except Exception as e:
                        print(f"   Erro: {e}")
    
    except Exception as e:
        print(f"   Erro ao abrir ZIP: {e}")

if len(df_clima_recife) > 0:

    print(f" RECIFE: {len(df_clima_recife):,} registros climáticos")

    
    df_clima_recife.to_csv('dados_clima_recife_apenas.csv', index=False, encoding='utf-8')
    print("\n Arquivo salvo: dados_clima_recife_apenas.csv")
    
    print("\nPeríodo dos dados:")
    print(f"  De: {df_clima_recife['Data'].min()}")
    print(f"  Até: {df_clima_recife['Data'].max()}")

else:

    print("  ESTAÇÃO DE RECIFE NÃO ENCONTRADA NO ZIP DE 2025")

    print("\nVocê precisa baixar os ZIPs dos anos anteriores (2019-2024)")
    print("ou usar os dados climatológicos médios.")
    print("\n SOLUÇÃO: Vou criar dados sintéticos baseados nas outras estações de PE")