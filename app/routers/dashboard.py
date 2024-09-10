from fastapi import Depends,APIRouter,FastAPI,HTTPException,status
from sqlalchemy import or_,and_
from sqlalchemy.sql import func,case
from typing import List
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas import UserResponse,UserCreate,UserUpdate
from app.models import User,Friendship
from app.utils import hash_password
from app.oauth2 import get_current_user




router=APIRouter(prefix="/dashboard",tags=["Dashboard"])


@router.get("/")
def dashboard(db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    amounts=db.query(
    func.sum(Friendship.amount).label("total_amount"),
    func.sum(
        case(
            (Friendship.amount < 0, Friendship.amount), 
            else_=0
        )
    ).label("total_amount_you_owe"),
    func.sum(
        case(
            (Friendship.amount > 0, Friendship.amount), 
            else_=0
        )
    ).label("total_amount_you_are_owed")
    ).filter(Friendship.user_id == current_user.id).first()
    
    return {"total_amount":amounts[0],"total_amount_you_owe":amounts[1],"total_amount_you_are_owed":amounts[2]}

@router.get("/expenses")
def dashboard_expenses(db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    list_friends_you_owe=db.query(User,Friendship.amount.label("amount")).join(Friendship,onclause=User.id==Friendship.friend_id).filter(and_(Friendship.user_id==current_user.id,Friendship.amount!=0)).all()
    return [{"friend":friend[0],"amount":friend[1]} for friend in list_friends_you_owe]
# @router.get("/expense")
# def you_are_owed(db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
#     list_friends_you_are_owed=db.query(User,Friendship.am{"friend":friend[0],"amount":friend[1]}ount.label("amount")).join(Friendship,onclause=User.id==Friendship.friend_id).filter(and_(Friendship.user_id==current_user.id)).all()
#     return list_friends_you_are_owed