
from fastapi import FastAPI, HTTPException
import uvicorn
from connection import MongoConnection
from userscema import listusers_serial,userindvidual_serial
from models import  user,loginuser
import jwt

app = FastAPI()
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000)
Client = MongoConnection()

@app.post("/createUser") 
def createUser(person:user):
    try:
        Client["users"].insert_one(dict(person))
        return "User Registered"
    except Exception:
        raise HTTPException(status_code=502, detail="DB connection failed")

@app.get("/login")
def loginUser(person:loginuser):
    try:
        user = userindvidual_serial(Client["users"].find_one(dict(person)))
        token = jwt.encode({
            "id" : user["id"]
        },"secret","HS256")
        db_token=Client["activeTokens"].find_one({"token":token})
        if db_token == None : Client["activeTokens"].insert_one({"token":token})
        return {"token":token}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=502, detail="DB connection failed")