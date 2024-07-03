from fastapi import APIRouter,FastAPI,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User,Friendship
from app.oauth2 import get_current_user

router= APIRouter(prefix="/friendships")


@router.post("/add")
def add_friend(friend_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    forward_friend=Friendship(user_id=current_user.id,friend_id=friend_id)
    db.add(forward_friend)    
    backward_friend=Friendship(user_id=friend_id,friend_id=current_user.id)
    db.add(backward_friend)
    db.commit()

    return {"messege":"friendship successful"}
@router.post("/delete")
def remove_friend(friend_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    forward_friend=Friendship(user_id=current_user.id,friend_id=friend_id)
    db.delete(forward_friend)    
    backward_friend=Friendship(user_id=friend_id,friend_id=current_user.id)
    db.delete(backward_friend)
    db.commit()

    return {"messege":"friendship successfully remove"}