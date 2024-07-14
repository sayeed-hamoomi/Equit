from fastapi import FastAPI,APIRouter,Depends,HTTPException,status
from app.database import get_db
from app.schemas import CalculateExpense,SplitType,CalculateExpenseResponse,AddExpense,ListExpenseResponse,ExpenseResponse
from sqlalchemy.orm import Session
from app.models import Expense,Split,User
from app.oauth2 import get_current_user
from typing import List

router=APIRouter(prefix="/expenses")


@router.post("/calculate",response_model=CalculateExpenseResponse)
def calculate_expense(expense:CalculateExpense):
    left=0
    splits=[]
    if expense.split_type ==SplitType.by_amount:
        left=expense.amount
        for split in expense.split:
            amount_owed=split.share
            left-=split.share
            splits.append({
                "participant_id":split.participant_id,
                "share":split.share,
                "amount_owed":amount_owed
            })

    elif expense.split_type ==SplitType.by_percentage:
        left=100
        for split in expense.split:
            amount_owed=expense.amount*split.share/100
            left-=split.share
            splits.append({
                "participant_id":split.participant_id,
                "share":split.share,
                "amount_owed":amount_owed
            })
    elif expense.split_type ==SplitType.equally:
        left=0
        for split in expense.split:
            amount_owed=expense.amount/len(expense.split)
            splits.append({
                "participant_id":split.participant_id,
                "share":amount_owed,
                "amount_owed":amount_owed
            })

    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail= "please select a valid split_type")

    return {"amount":expense.amount,"split_type":expense.split_type,"left":left,"split":splits}        

        

@router.post("/")
def create_expense(expense:AddExpense,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    if expense.left !=0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="unbalance expense")
    new_expense=Expense(description=expense.description,amount=expense.amount,split_type=expense.split_type,payer_id=expense.payer_id,notes=expense.notes)
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    expense_id=new_expense.id
    for split in expense.split:
        new_split=Split(expense_id=expense_id,participant_id=split.participant_id,amount_owed=split.amount_owed)
        db.add(new_split)

    db.commit()
    return {":messege":"expense added successfully"}
# @router.get("/")
@router.get("/",response_model=List[ListExpenseResponse])
def list_expenses(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    expenses=db.query(Expense).join(Split,Expense.id==Split.expense_id).join(User,Expense.payer_id==User.id).filter(Split.participant_id==current_user.id).all()
    return expenses
@router.get("/{id}",response_model=ExpenseResponse)
def get_expense(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    expense=db.query(Expense).join(Split,Expense.id==Split.expense_id).filter(Split.participant_id==current_user.id,Expense.id==id).first()
    if not expense :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="no expense with this id")
    
    
    return expense
      

