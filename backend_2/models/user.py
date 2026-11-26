from typing import List, Union

from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    confirm_password: str
    
class UserDetailsView(BaseModel):
    firstName: str
    lastName: str
    email: str
    phone: str 
    
class UserDetailsCreate(BaseModel):
    firstName: str
    lastName: str
    email: str
    phone: str 

class UserDetailsUpdate(BaseModel):
    firstName: str | None
    lastName: str | None
    email: str | None
    phone: str | None

class UserView(BaseModel):
    id: int
    username: str
