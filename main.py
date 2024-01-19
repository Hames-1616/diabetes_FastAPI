
from fastapi import FastAPI, Header
import uvicorn
from connection import MongoConnection
from userscema import userindvidual_serial
from models import *
import jwt
from badrequestfunction import badrequest
from bson import ObjectId

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
def UsermedDetails(userDetails:BasicUserInfo,token:str=Header()):
       usr = Client["activeTokens"].find_one({"token":token})
       if usr :
              user_id = jwt.decode(token,"secret","HS256")
              user_details = userindvidual_serial(Client["users"].find_one({"_id":ObjectId(user_id["id"])}))
              email = user_details["email"]
              db_details = dict(dbUserInfo(info=dict(userDetails),email=user_details["email"]))
              print(db_details)
              existing_details = Client["basicInfo"].find_one({"email":email})
              if existing_details :
                     Client["basicInfo"].update_one({"email":email},{"$set":{"info":dict(userDetails)}},upsert=True)
              else :
                     Client["basicInfo"].insert_one(db_details)
       else:
              return badrequest("Session Not Valid")
       
@app.get("/basicInfoVerify")
def userinfostatus(token:str=Header()):
       usr = Client["activeTokens"].find_one({"token":token})
       if usr :
              user_id = jwt.decode(token,"secret","HS256")
              userDetails = userindvidual_serial(Client["users"].find_one({"_id":ObjectId(user_id["id"])}))
              basicinfoCheck = dict(Client["basicInfo"].find_one({"email":userDetails["email"]}))
              if basicinfoCheck :
                     return True
              else :
                     return badrequest("Details are Not present")
       else :
              return badrequest("Session is Not Valid")