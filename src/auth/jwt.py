from datetime import datetime, timedelta
from jose import jwt
from core.config import settings
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_tok(user_id:int) -> str:
    
    time_exp=datetime.utcnow()+timedelta(minutes=30)
    payload={
        "sub": str(user_id),
        "exp": time_exp
    }
    token_key=jwt.encode(payload,settings.SECRET_KEY,algorithm="HS256")
    return token_key

def verify_tok(token_key:str):
    try :
        decod_tok=jwt.decode(token_key,settings.SECRET_KEY,algorithms=["HS256"])
    except:
        raise HTTPException(status_code=401, detail="no token")
    return decod_tok
    
    

