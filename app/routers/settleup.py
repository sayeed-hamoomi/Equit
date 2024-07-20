from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.oauth2 import get_current_user
from app.schemas import AddSettleup
from app.models import Settleup,Transaction
from datetime import datetime

router=APIRouter(prefix="/settleup")


@router.post("/")
def create_settleup(settleup:AddSettleup,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
   transaction=Transaction(sender_id=settleup.payer_id,receiver_id=settleup.receiver_id,amount=settleup.amount,created_at=datetime.now())
   db.add(transaction)
   db.commit()
   new_settleup=Settleup(payer_id=settleup.payer_id,receiver_id=settleup.receiver_id,amount=settleup.amount,notes=settleup.notes)
   db.add(new_settleup)
   db.commit()
   db.refresh(new_settleup)
   return new_settleup