from pydantic import BaseModel,EmailStr
from typing import Optional,List
from enum import Enum
from decimal import Decimal
from datetime import datetime

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

class CalculateSplit(BaseModel):
    participant_id: int
    share: int

class CalculateSplitResponse(CalculateSplit):
    amount_owed:int

class CalculateExpense(BaseModel):
    amount:int
    split_type: SplitType
    split:List[CalculateSplit]


class CalculateExpenseResponse(BaseModel):
    amount:int
    split_type: SplitType
    left:int
    split:List[CalculateSplitResponse]




class AddExpense(CalculateExpenseResponse):
    description:str
    payer_id:int
    notes:Optional[str]=None


class ListExpenseResponse(BaseModel):
    id:int
    description:str
    amount:int
    split_type: SplitType
    notes:str
    payer_id:int
    payer:UserResponse
class SplitRespose(BaseModel):
    id:int
    participant_id:int
    amount_owed:int
    is_settled:bool
    participant:UserResponse
    # settled_at:datetime
    # created_at:datetime
    # updated_at:datetime    
class ExpenseResponse(ListExpenseResponse):
    splits:List[SplitRespose]    

# class AddSettleup(BaseModel):
#     payer_id:int
#     receiver_id:int
#     amount:int
#     notes:str
#     settled_at:datetime
class AddTransaction(BaseModel):
    sender_id:int
    receiver_id:int
    amount:Decimal
    notes:Optional[str]
class ViewFriendResponce(UserResponse):
    id:int