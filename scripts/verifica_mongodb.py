# scripts/verifica_mongodb.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from api.database import get_database

db = get_database()

print("Collections disponiveis:")
for collection_name in db.list_collection_names():
    count = db[collection_name].count_documents({})
    print(f"  {collection_name}: {count} documentos")

print("\nVerificando casos_integrados:")
sample = list(db.casos_integrados.find().limit(3))
if sample:
    print("Primeiros registros:")
    for doc in sample:
        print(f"  {doc}")
else:
    print("  Collection vazia")

print("\nVerificando anos disponiveis:")
anos = db.casos_integrados.distinct("ANO")
print(f"  Anos: {anos}")

print("\nVerificando casos_por_bairro:")
sample_bairro = list(db.casos_por_bairro.find().limit(3))
if sample_bairro:
    print("Primeiros registros:")
    for doc in sample_bairro:
        print(f"  {doc}")
else:
    print("  Collection vazia")