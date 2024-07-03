from app.database import Base
from sqlalchemy import Column,Integer,String,ForeignKey,Numeric,DateTime,func,Enum,Boolean
from app.schemas import SplitType




class User(Base):
    __tablename__="users"
    id= Column(Integer,primary_key=True)
    name=Column(String)
    email=Column(String,unique=True,nullable=False)
    password=Column(String,nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Friendship(Base):
    __tablename__="friendships"
    user_id=Column(Integer,ForeignKey("users.id",ondelete='CASCADE'),primary_key=True)
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
class Split(Base):
    __tablename__="splits"
    id=Column(Integer,primary_key=True)
    expense_id=Column(Integer,ForeignKey("expenses.id",ondelete="CASCADE"),nullable=False)
    participate_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    amount_owed=Column(Numeric,nullable=False)
    is_settled=Column(Boolean,default=False)
    settled_at=Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())



