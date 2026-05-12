from pymongo import MongoClient
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

print("Conectando ao MongoDB Atlas...")
client = MongoClient(MONGODB_URL)
db = client[DATABASE_NAME]

print("Populando MongoDB com dados históricos...")

df = pd.read_csv('data/processed/dados_integrados_dengue_clima.csv')

registros = df.to_dict('records')
db.casos_dengue.delete_many({})
result = db.casos_dengue.insert_many(registros)

print(f"✓ Inseridos {len(result.inserted_ids)} registros na collection 'casos_dengue'")
print("✓ MongoDB populado com sucesso!")

client.close()