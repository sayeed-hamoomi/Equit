from jose import JWTError,jwt
from app.config import settings
from datetime import datetime,timedelta
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from app.models import User
from sqlalchemy.orm import Session
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

secret_key=settings.secret_key
algorithm=settings.algorithm
access_token_expire_minutes=settings.access_token_expire_minutes

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=access_token_expire_minutes)
    to_encode.update({"exp":expire})
    token=jwt.encode(to_encode,secret_key,algorithm=algorithm)
    return token
def verify_access_token(token:str,credential_exceptions):
    try:
        token_data=jwt.decode(token=token,key=secret_key,algorithms=[algorithm])
    except JWTError:
        raise credential_exceptions
    user_id=token_data.get("user_id")
    if not user_id:
        raise credential_exceptions
    return user_id
def get_current_user(token:str=Depends(oauth2_scheme),db: Session = Depends(get_db)):
    credential_exceptions= HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid token")
    user_id= verify_access_token(token=token,credential_exceptions=credential_exceptions)
    user=db.query(User).filter(User.id==user_id).first()
    if not user:
        raise credential_exceptions
    return user
