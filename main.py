
from fastapi import FastAPI, HTTPException, Header
import uvicorn
from connection import MongoConnection
from userscema import listusers_serial,userindvidual_serial
from models import *
import jwt
from badrequestfunction import badrequest

app = FastAPI()
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000)
Client = MongoConnection()

@app.post("/createUser") 
def createUser(person:user):
        user = Client["users"].find_one({"email":person.email})
        if user : badrequest("User Already Exists")
        Client["users"].insert_one(dict(person))
        return "User Registered"


@app.get("/login")
def loginUser(person:loginuser):
            user = Client["users"].find_one(dict(person))
            if user:
                user = userindvidual_serial(user)
                token = jwt.encode({
                "id" : user["id"]
                },"secret","HS256")
                db_token=Client["activeTokens"].find_one({"token":token})
                if db_token == None : Client["activeTokens"].insert_one({"token":token})
                return {"token":token}
            else :
                badrequest("User Not Found")
      
  
    
@app.post("/signOut")
def signout(token:str=Header()):
        db_token = Client["activeTokens"].find_one({"token":token})
        if db_token == None : return badrequest("Not Found")
        return "Deleted"

@app.post("/basicInfo")
def UsermedDetails(userDetails:BasicUserInfo(),token:str=Header()):
       usr:user = Client["activeTokens"].find_one({"token":token})
       if user : 
              user_details = Client["basicInfo"].find_one({"email":usr.email})
              db_details = dbUserInfo(info=user_details,email=usr.email)
              if user_details :
                     Client["basicInfo"].update_one(dict(db_details))
              else:
                     Client["basicInfo"].insert_one(dict(db_details))
       else:
              return badrequest("Session Not Valid")
        

