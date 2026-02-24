
from pydantic import BaseModel,ConfigDict


class UserBase(BaseModel): #base schemas
    
    name:str
    email:str
    
class UserCreate(UserBase): #schema for new user 
    password:str

class UserResponse(UserBase):#schema for returning user data
    id:int
    enabled:bool
    model_config=ConfigDict(from_attributes=True)