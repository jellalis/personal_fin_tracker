from sqlalchemy import Column, Integer, String, Boolean,Numeric
from src.db.database import Base
from sqlalchemy import ForeignKey



class Budget(Base):
    __tablename__= 'budget'
    
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    amount=Column(Numeric(precision=10, scale=2), nullable=False)
    category_id=Column(Integer,ForeignKey("categories.id"),nullable=False)
    month=Column(Integer,nullable=False)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
