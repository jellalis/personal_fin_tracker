from sqlalchemy import Column, Integer, String, Boolean,Numeric
from sqlalchemy import  Date, DateTime
from datetime import datetime,timezone
from src.db.database import Base
from sqlalchemy import ForeignKey

class Transaction(Base):
    __tablename__= 'transactions'
    id=Column(Integer, primary_key=True, index=True)
    category_id=Column(Integer,ForeignKey("categories.id"),nullable=False)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    amount=Column(Numeric(precision=10, scale=2), nullable=False)
    type=Column(String,nullable=False)
    transaction_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))