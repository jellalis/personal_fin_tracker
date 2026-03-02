from passlib.context import CryptContext



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pass(password:str):
    hash_pass=pwd_context.hash(password)
    return hash_pass    
def ver_pass(password:str,hash_pass):
    ver=pwd_context.verify(password, hash_pass)
    return ver
    