from fastapi import APIRouter,FastAPI,HTTPException,status,Depends
from app.schemas import UserLogin
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.utils import verify_password
from app.oauth2 import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router=APIRouter()

@router.post("/login",tags=["authentication"])
def user_login(user_credential:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==user_credential.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalid credentials")
    if not verify_password(user_credential.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalid credentials")
    token=create_access_token({"user_id":user.id})
    return{"access_token":token,"token_type":"Bearer"}
