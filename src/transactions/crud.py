from sqlalchemy.orm import Session
from transactions.models import Transaction
from transactions.schemas import TransactionCreate
from fastapi import HTTPException
from categories.crud import get_categ_or_404
#create transaction

def create_transaction(db: Session, user_id: int, transaction_data: TransactionCreate):
    # verify category exists
    category = get_categ_or_404(db, transaction_data.category_id)
    # Security: only allow own categories or default (NULL) categories
    # Prevents User B from linking transactions to User A's private categories
    if category.user_id != user_id and category.user_id is not None:
        raise HTTPException(status_code=404, detail="no category with this id")
    new_transaction = Transaction(
        user_id=user_id,
        category_id=transaction_data.category_id,
        amount=transaction_data.amount,
        type=transaction_data.type,
        transaction_date=transaction_data.transaction_date,
        description=transaction_data.description
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

def get_transactions(db:Session,user_id:int):
    transactions=db.query(Transaction).filter(Transaction.user_id==user_id).all()
    return transactions

def get_transaction_or_404(db:Session,user_id:int,transaction_id:int):
    transaction=db.query(Transaction).filter(Transaction.id==transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404,detail="Transaction not found")
    elif transaction.user_id!=user_id:
        raise HTTPException(status_code=404,detail="Transaction not found")
    return transaction
    
def delete_transaction(db:Session,user_id:int,transaction_id:int):
    transaction_del=get_transaction_or_404(db,user_id,transaction_id)
    db.delete(transaction_del)
    db.flush()
    db.expunge(transaction_del)
    db.commit()
    return transaction_del