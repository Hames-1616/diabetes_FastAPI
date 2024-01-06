from fastapi import HTTPException


def badrequest(value:str):
    raise HTTPException(status_code=404, detail=value)