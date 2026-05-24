from pydantic import BaseModel,ConfigDict



# UserBase holds fields shared by all user-related schemas
class UserBase(BaseModel):  # base schema
    name:str
    email:str

# UserCreate extends UserBase — adds 'password' only needed when registering a new user
# The router receives this schema, then passes it to crud.py which hashes the password
class UserCreate(UserBase):  # schema for new user
    password:str

# UserResponse is what the API returns — includes id and enabled, but intentionally omits password

class UserResponse(UserBase):  # schema for returning user data
    id:int
    enabled:bool
    model_config=ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    email:str
    password:str
