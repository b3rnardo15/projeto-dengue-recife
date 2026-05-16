# scripts/script-main.py
import subprocess
import sys
from pathlib import Path

def run_script(script_name):
   
    print(f"Executando: {script_name}")
  
    
    result = subprocess.run([sys.executable, f"scripts/{script_name}"], capture_output=False)
    
    if result.returncode != 0:
        print(f"Erro ao executar {script_name}")
        sys.exit(1)
    
    print(f"{script_name} concluido com sucesso")

print("\nPIPELINE COMPLETO - SISTEMA PREDICAO DENGUE RECIFE\n")

scripts = [
    "01_consolidar_dados_dengue.py",
    "04_integracao_dados.py",
    "converter_codigos_bairros.py",
    "05_treinar_modelo.py",
    "popular_mongodb_completo.py",
]

for script in scripts:
    script_path = Path(f"scripts/{script}")
    if not script_path.exists():
        print(f"Script {script} nao encontrado, pulando...")
        continue
    
    run_script(script)


print("PIPELINE COMPLETO EXECUTADO")

print("\nArquivos gerados:")
print("  data/processed/dengue_consolidado_2019_2025.csv")
print("  data/processed/casos_dengue_bairros_2020_2025.csv")
print("  data/processed/dados_integrados_dengue_clima.csv")
print("\nMongoDB populado")
print("\nRodar API:")
print("  uvicorn api.main:app --reload")