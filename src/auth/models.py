from sqlalchemy import Column, Integer, String, Boolean
from db.database import Base  


class User(Base):
    __tablename__= 'users'

 
    id=Column(Integer,primary_key=True,index=True)

    name=Column(String,nullable=False)  # required — DB will reject NULL values


    email=Column(String,unique=True,nullable=False,index=True)

    hashed_password=Column(String,nullable=False)  # we NEVER store plain text passwords


    enabled=Column(Boolean,default=True)
