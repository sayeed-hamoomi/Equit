from fastapi import APIRouter,FastAPI,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User,Friendship
from app.oauth2 import get_current_user
from typing import List
from app.schemas import UserResponse,ViewFriendResponce

router= APIRouter(prefix="/friendships")


@router.post("/add")
def add_friend(friend_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    forward_friend=Friendship(user_id=current_user.id,friend_id=friend_id)
    db.add(forward_friend)    
    backward_friend=Friendship(user_id=friend_id,friend_id=current_user.id)
    db.add(backward_friend)
    db.commit()
    return {"messege":"friendship successful"}
@router.get("/",response_model=List[UserResponse])
def view_friends(db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    friends=db.query(User).join(Friendship,User.id==Friendship.user_id).filter(Friendship.friend_id==current_user.id)
    return friends
@router.get("/friend/{id}",response_model=ViewFriendResponce)
def view_friend(id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    friend=db.query(User).filter(User.id==id).join

    if not friend :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="no friend with this id")
    return friend
@router.delete("/delete")
def remove_friend(friend_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    forward_friend=db.query(Friendship).filter(Friendship.user_id==current_user.id,Friendship.friend_id==friend_id).delete(synchronize_session=False)
    backward_friend=db.query(Friendship).filter(Friendship.user_id==friend_id,Friendship.friend_id==current_user.id).delete(synchronize_session=False)
    db.commit()

    return {"messege":"friendship successfully remove"}