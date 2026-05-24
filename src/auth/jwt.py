from datetime import datetime, timedelta
from jose import jwt
from core.config import settings
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer

# OAuth2PasswordBearer is a FastAPI dependency that extracts the Bearer token from the
# Authorization header of incoming requests (Authorization: Bearer <token>)
# tokenUrl tells Swagger UI where to send the login request for the "Authorize" button
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_tok(user_id:int) -> str:
    # Token expires 30 minutes from now — a balance between security (short) and convenience (not too short)
    time_exp=datetime.utcnow()+timedelta(minutes=30)

    # The JWT payload (also called "claims") — data we embed inside the signed token
    # "sub" (subject) is the standard JWT field for identifying the user — must be a string
    # "exp" (expiration) is enforced automatically by jose during jwt.decode()
    payload={
        "sub": str(user_id),  # str() because JWT standard requires sub to be a string, not int
        "exp": time_exp
    }

    # jwt.encode() signs the payload with our SECRET_KEY using the HS256 algorithm
    # The token is readable by anyone (it's base64) but the signature proves it wasn't tampered with
    token_key=jwt.encode(payload,settings.SECRET_KEY,algorithm="HS256")
    return token_key

def verify_tok(token_key:str):
    try:
        # jwt.decode() does two things automatically:
        # 1. Verifies the signature (was this token signed with our SECRET_KEY?)
        # 2. Checks the expiration (is the token still valid?)
        # If either check fails, it raises an exception caught below
        decod_tok=jwt.decode(token_key,settings.SECRET_KEY,algorithms=["HS256"])
    except:
        raise HTTPException(status_code=401, detail="no token")
    # Returns the decoded payload dict, e.g. {"sub": "1", "exp": 1234567890}
    return decod_tok
