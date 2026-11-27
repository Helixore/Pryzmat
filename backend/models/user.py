from datetime import date
from db_models.models import UserRole
from typing import List, Union

from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    role: UserRole
    firstName: str
    lastName: str
    PESEL: str
    address: str
    email: str
    dateOfBirth: date | None = None

class UserSetupPassword(BaseModel):
    flogin_code: str
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
    PESEL: str | None

class UserView(BaseModel):
    id: int
    username: str
    role: str
