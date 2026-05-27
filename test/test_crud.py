from auth.crud import create_user
from auth.schemas import UserCreate
from auth.hashing import ver_pass
import pytest
from fastapi import HTTPException
from auth.crud import get_user_or_404,delete_user
def test_create_user(db):
    
    user_data=UserCreate(
        name="Panos",
        email="Panos@gmail.com",
        password="Panos"
        
    )
    created=create_user(db,user_data)
    
    assert created.id is not None
    assert created.email=="Panos@gmail.com"
    assert ver_pass("Panos",created.hashed_password)
    


def test_get_user_not_found(db):
    with pytest.raises(HTTPException) as exc_info:
        get_user_or_404(db,user_id=10)
    assert  exc_info.value.status_code==404

def test_delete_user(db):
    user_data=UserCreate(
    name="Panos",
    email="Panos@gmail.com",
    password="Panos"
        
    )
    created=create_user(db,user_data)
    delete_user(db,created.id)
    with pytest.raises(HTTPException) as exc_info:
        get_user_or_404(db,user_id=created.id)
    assert exc_info.value.status_code==404