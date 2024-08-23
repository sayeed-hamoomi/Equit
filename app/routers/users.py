from fastapi import Depends,APIRouter,FastAPI,HTTPException,status
from sqlalchemy import or_
from typing import List
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas import UserResponse,UserCreate,UserUpdate
from app.models import User
from app.utils import hash_password
from app.oauth2 import get_current_user


router=APIRouter(prefix="/users")


@router.get("/",response_model=List[UserResponse])
def all_users(search:str="",db: Session = Depends(get_db)):
    users=db.query(User).filter(or_(User.name.ilike(f"%{search}%"),User.email.ilike(f"%{search}%"))).all()
    return users

@router.post("/",response_model=UserResponse)
def create_user(user:UserCreate,db: Session = Depends(get_db)):
    user.password=hash_password(user.password)
    new_user=User(name=user.name,email=user.email,password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
@router.patch("/{id}")
def update_user(id:int,user:UserUpdate,db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    user_query=db.query(User).filter(User.id==id)
    if not user_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user with id does not exist")
    updated=user_query.update(user.dict(),synchronize_session=False)
    db.commit()
    return {"messege":"successfully updated"}
@router.delete("/{id}")
def delete_user(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    user_query=db.query(User).filter(User.id==id)
    if not user_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user with id does not exist")
    deleted=user_query.delete(synchronize_session=False)
    db.commit()
    return {"messege":"successfully deleted"}

