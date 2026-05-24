from passlib.context import CryptContext

# CryptContext manages password hashing — configured to use the bcrypt algorithm
# deprecated="auto" → passlib can automatically re-hash passwords if the scheme changes in the future

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pass(password:str):
    # Converts a plain text password into a bcrypt hash
    # Always call this before storing any password in the database — never store plain text
    hash_pass=pwd_context.hash(password)
    return hash_pass

def ver_pass(password:str,hash_pass):
    # Compares a plain text password against a stored bcrypt hash
    # Returns True if they match, False if they don't
    
    ver=pwd_context.verify(password, hash_pass)
    return ver
