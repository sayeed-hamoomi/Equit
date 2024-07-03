from pydantic import BaseModel,EmailStr
from typing import Optional
from enum import Enum

class SplitType(str,Enum):
    equally="equally"
    by_amount="by_amount"
    by_percentage="by_percentage"

class UserBase(BaseModel):
   
    email:EmailStr
class UserCreate(UserBase):
    name:str
    password:str
class UserResponse(UserBase):
    id:int
    name:str
    email:EmailStr
class UserUpdate(BaseModel):
    name:Optional[str]
    email:Optional[EmailStr]
    password:Optional[str]
class UserLogin(BaseModel):
    email:EmailStr
    password:str

# class AddFriend(BaseModel):
        