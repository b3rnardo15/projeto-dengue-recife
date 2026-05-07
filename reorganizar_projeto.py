import os
import shutil
from pathlib import Path

def criar_estrutura():
    
    diretorios = [
        'data/raw',
        'data/processed',
        'models',
        'scripts',
        'api',
        'outputs',
        'archive'
    ]
    
    print("Criando estrutura de diretorios...")
    for dir_path in diretorios:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"  Criado: {dir_path}/")
    
    mapeamento = {
        '01_consolidar_dados_dengue.py': 'scripts/01_consolidar_dados_dengue.py',
        '02_baixar_dados_clima_inmet.py': 'scripts/02_baixar_dados_clima_inmet.py',
        '03_analise_exploratoria.py': 'scripts/03_analise_exploratoria.py',
        '04_integracao_dados.py': 'scripts/04_integracao_dados.py',
        '11_modelo_producao_final.py': 'scripts/05_treinar_modelo.py',
    }
    
    arquivar = [
        '05_modelagem_preditiva.py',
        '06_melhorias_modelo.py',
        '07_predicao_semanas_futuras.py',
    ]
    
    print("\nMovendo scripts principais...")
    for origem, destino in mapeamento.items():
        if os.path.exists(origem):
            shutil.copy2(origem, destino)
            print(f"  {origem} -> {destino}")
    
    print("\nArquivando scripts experimentais...")
    for arquivo in arquivar:
        if os.path.exists(arquivo):
            shutil.move(arquivo, f'archive/{arquivo}')
            print(f"  {arquivo} -> archive/")
    
    dados_processados = [
        'dengue_consolidado_2019_2025.csv',
        'dados_clima_recife_apenas.csv',
        'dataset_dengue_clima_integrado.csv'
    ]
    
    print("\nOrganizando dados processados...")
    for arquivo in dados_processados:
        if os.path.exists(arquivo):
            shutil.move(arquivo, f'data/processed/{arquivo}')
            print(f"  {arquivo} -> data/processed/")
    
    modelos = [
        'modelo_dengue_emprel_producao.pkl',
        'modelo_dengue_xgboost.pkl',
        'modelo_dengue_producao.pkl'
    ]
    
    print("\nOrganizando modelos...")
    for arquivo in modelos:
        if os.path.exists(arquivo):
            shutil.move(arquivo, f'models/{arquivo}')
            print(f"  {arquivo} -> models/")
    
    graficos = [
        'sazonalidade_dengue.png',
        'correlacao_dengue_clima.png',
        'comparacao_modelos.png',
        'predicao_melhor_modelo.png',
        'modelo_producao_emprel.png',
        'importancia_features_limpo.png',
        'predicao_4_8_semanas.png'
    ]
    
    print("\nOrganizando outputs...")
    for arquivo in graficos:
        if os.path.exists(arquivo):
            shutil.move(arquivo, f'outputs/{arquivo}')
            print(f"  {arquivo} -> outputs/")
    
    print("\nEstrutura reorganizada com sucesso!")
    print("\nProximos passos:")
    print("1. Revisar scripts em scripts/")
    print("2. Commitar no Git")
    print("3. Desenvolver API em api/")

if __name__ == "__main__":
    criar_estrutura()