from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from db.database import get_db
from auth.jwt import verify_tok
from transactions.models import Transaction, TransactionType

router = APIRouter(prefix="/summary", tags=["reports"])

@router.get("")
def get_summary(user_id: int = Depends(verify_tok), db: Session = Depends(get_db)):
    # Sum all income transactions for this user
    income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id,
        Transaction.type == TransactionType.income
    ).scalar() or 0

    # Sum all expense transactions for this user
    expense = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id,
        Transaction.type == TransactionType.expense
    ).scalar() or 0

    return {
        "balance": float(income - expense),
        "income": float(income),
        "expense": float(expense),
        "currency": "EUR",
    }
