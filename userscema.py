def userindvidual_serial(user) -> dict:
    return {
        "id":str(user["_id"]),
        "username":user["username"],
        "email":user["email"],
        "password":user["password"]
        
    } 

def listusers_serial(users)->list:
    return [userindvidual_serial(user) for user in users]

def activeToken(token) -> dict :
    return {
        "token":token["token"]
    }
def allactiveTokens(tokens) -> list :
    return [activeToken(token) for token in tokens]