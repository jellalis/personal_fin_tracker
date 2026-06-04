from pydantic import BaseModel,ConfigDict
from decimal import Decimal
from datetime import date, datetime
from enum import Enum
from typing import Optional

class TransactionType(str, Enum):
    income = "income"
    expense = "expense"
    
class TransactionBase(BaseModel):
    category_id:int
    amount:Decimal
    type:TransactionType  
    description:Optional[str] = None 
    transaction_date:date     
class TransactionCreate(TransactionBase) :
    pass

class TransactionResponse(TransactionBase):
    id:int
    created_at:datetime  
    user_id:int    
    model_config=ConfigDict(from_attributes=True)
    
