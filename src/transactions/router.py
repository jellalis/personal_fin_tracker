from transactions.crud import create_transaction,get_transaction_or_404,delete_transaction,get_transactions
from transactions.schemas import TransactionCreate,TransactionResponse
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends
from db.database import get_db

from auth.jwt import oauth2_scheme,verify_tok

router=APIRouter()

@router.post("/transactions",response_model=TransactionResponse,status_code=201)
def post_router(transactions_data:TransactionCreate,db:Session=Depends(get_db),token:str=Depends(oauth2_scheme)):
    payload=verify_tok(token)
    user_id=int(payload["sub"])
    new_transaction=create_transaction(db,user_id,transactions_data)
    return new_transaction
@router.get("/transactions",response_model=list[TransactionResponse])
def get_routers(db:Session=Depends(get_db),token:str=Depends(oauth2_scheme)):
    payload=verify_tok(token)
    user_id=int(payload["sub"])
    transactions=get_transactions(db,user_id)
    return transactions
@router.get("/transactions/{transaction_id}",response_model=TransactionResponse)
def get_router(transaction_id:int,db:Session=Depends(get_db),token:str=Depends(oauth2_scheme)):
    payload=verify_tok(token)
    user_id=int(payload["sub"])
    transaction=get_transaction_or_404(db,user_id,transaction_id)
    return transaction
@router.delete("/transactions/{transaction_id}",response_model=TransactionResponse)
def del_router(transaction_id:int,db:Session=Depends(get_db),token:str=Depends(oauth2_scheme)):
    payload=verify_tok(token)
    user_id=int(payload["sub"])
    del_transaction=delete_transaction(db,user_id,transaction_id)
    return del_transaction