from fastapi import HTTPException
from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv

def MongoConnection():
    load_dotenv()
    db_url = os.getenv("DB")
    try:
        Client = MongoClient(db_url)
        db = Client.diabetes
        return db
    except Exception as e:
        raise HTTPException(status_code=502, detail="DB connection failed")
