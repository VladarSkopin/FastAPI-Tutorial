# API Models

from pydantic import BaseModel


class UserCreate(BaseModel):
    name:str
    email:str
    age:int
    role:str


class UserResponse(BaseModel):
    id:int  # will match Id from Db
    name:str
    age:int
    email:str
    role:str

    class Config:
        from_attributes = True

