from fastapi import FastAPI,APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AddTransaction
from app.models import Transaction,Friendship

router= APIRouter(prefix="/transactions")



@router.post("/")
def add_transaction(transaction:AddTransaction,db:Session=Depends(get_db)):
    new_transaction=Transaction(sender_id=transaction.sender_id,receiver_id=transaction.receiver_id,amount=transaction.amount,notes=transaction.notes)
    db.add(new_transaction)
    db.query(Friendship).filter(Friendship.user_id==transaction.sender_id,Friendship.friend_id==transaction.receiver_id).update({"amount": Friendship.amount+transaction.amount},synchronize_session=False)
    db.query(Friendship).filter(Friendship.user_id==transaction.receiver_id,Friendship.friend_id==transaction.sender_id).update({"amount": Friendship.amount-transaction.amount}, synchronize_session=False)  
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

