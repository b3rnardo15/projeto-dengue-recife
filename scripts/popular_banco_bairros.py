import pandas as pd
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from api.database import get_database

print("Populando MongoDB com dados de bairros...")

db = get_database()
collection = db['casos_por_bairro']

df = pd.read_csv('data/processed/casos_dengue_bairros_2020_2025.csv')

print(f"Total de registros a inserir: {len(df)}")
print(f"Período: {df['ANO'].min()} - {df['ANO'].max()}")
print(f"Bairros únicos: {df['BAIRRO'].nunique()}")

collection.drop()
print("Coleção anterior removida")

registros = df.to_dict('records')
resultado = collection.insert_many(registros)

print(f"\n {len(resultado.inserted_ids)} documentos inseridos!")

print("\nCriando índices...")
collection.create_index([("ANO", 1), ("SEMANA", 1)])
collection.create_index([("BAIRRO", 1)])
collection.create_index([("ANO", 1), ("BAIRRO", 1)])

print(" Índices criados!")

print("\nVerificação:")
total = collection.count_documents({})
print(f"Total de documentos no banco: {total}")

print("\nAmostra (primeiros 3 registros):")
for doc in collection.find().limit(3):
    print(f"  {doc['ANO']}-S{doc['SEMANA']} | {doc['BAIRRO']}: {doc['CASOS']} casos")

print("\nTop 5 bairros com mais casos:")
pipeline = [
    {"$group": {"_id": "$BAIRRO", "total": {"$sum": "$CASOS"}}},
    {"$sort": {"total": -1}},
    {"$limit": 5}
]
for resultado in collection.aggregate(pipeline):
    print(f"  {resultado['_id']}: {resultado['total']} casos")