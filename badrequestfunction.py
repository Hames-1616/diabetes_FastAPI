from fastapi import HTTPException


def badrequest(value:str):
    raise HTTPException(status_code=400, detail=value)