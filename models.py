from pydantic import BaseModel

class user(BaseModel):
    username:str
    email:str
    password:str

class loginuser(BaseModel):
    email:str
    password:str

class BasicUserInfo(BaseModel):
    gender:str
    variant : str
    blood : str

class dbUserInfo(BaseModel):
    info : BasicUserInfo
    email : str