from pymongo import MongoClient
from pymongo.database import Database
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "dengue_recife")

client = None
db = None

def get_database() -> Database:
    global client, db
    if db is None:
        client = MongoClient(MONGODB_URL)
        db = client[DATABASE_NAME]
    return db

def close_database():
    global client
    if client:
        client.close()