import joblib
from pathlib import Path

MODEL_PATH = Path("models/modelo_dengue_emprel_producao.pkl")

print("Carregando modelo...")
modelo = joblib.load(MODEL_PATH)

print(f"Tipo do modelo: {type(modelo)}")
print(f"Conteúdo: {modelo}")

if isinstance(modelo, dict):
    print("\nChaves do dicionário:")
    for key in modelo.keys():
        print(f"  - {key}: {type(modelo[key])}")