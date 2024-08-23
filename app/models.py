from app.database import Base
from sqlalchemy import Column,Integer,String,ForeignKey,Numeric,DateTime,func,Enum,Boolean,DECIMAL
from sqlalchemy.orm import relationship

from app.schemas import SplitType




class User(Base):
    __tablename__="users"
    id= Column(Integer,primary_key=True)
    name=Column(String)
    email=Column(String,unique=True,nullable=False)
    password=Column(String,nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    expenses = relationship("Expense", back_populates="payer")
    splits=relationship("Split",back_populates="participant")
    transactions_sent = relationship("Transaction", foreign_keys="[Transaction.sender_id]", back_populates="sender")
    transactions_received = relationship("Transaction", foreign_keys="[Transaction.receiver_id]", back_populates="receiver")



class Friendship(Base):
    __tablename__="friendships"
    user_id=Column(Integer,ForeignKey("users.id",ondelete='CASCADE'),primary_key=True)
    amount=Column(Numeric,nullable=False, server_default='0')
    friend_id=Column(Integer,ForeignKey("users.id",ondelete='CASCADE'),primary_key=True)
        

class Expense(Base):
    __tablename__="expenses"
    id=Column(Integer,primary_key=True)
    description=Column(String,nullable=False)
    amount=Column(Numeric,nullable=False)
    split_type=Column(Enum(SplitType),default=SplitType.equally,nullable=False)
    payer_id=Column(Integer,ForeignKey("users.id",ondelete='CASCADE'),nullable=False)
    notes=Column(String,nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    payer=relationship("User", back_populates="expenses")
    splits=relationship("Split",back_populates="expense")

class Split(Base):
    __tablename__="splits"
    id=Column(Integer,primary_key=True)
    expense_id=Column(Integer,ForeignKey("expenses.id",ondelete="CASCADE"),nullable=False)
    participant_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    amount_owed=Column(Numeric,nullable=False)
    is_settled=Column(Boolean,default=False)
    settled_at=Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    expense=relationship("Expense",back_populates="splits")
    participant=relationship("User",back_populates="splits")

# class Settleup(Base):
#     __tablename__="settleup"
#     id=Column(Integer,primary_key=True)
#     payer_id=Column(Integer,ForeignKey("users.id",ondelete='CASCADE'),nullable=False)
#     receiver_id=Column(Integer,ForeignKey("users.id",ondelete='CASCADE'),nullable=False)
#     amount=Column(Numeric,nullable=False)
#     settled_at=Column(DateTime(timezone=True), server_default=func.now())
#     notes=Column(String,nullable=True)

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    amount = Column(Numeric, nullable=False)
    notes=Column(String,nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    sender = relationship("User", foreign_keys=[sender_id], back_populates="transactions_sent")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="transactions_received")
