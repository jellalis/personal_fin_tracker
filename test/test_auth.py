import pytest
from fastapi import HTTPException
from auth.crud import create_user,get_user_or_404,delete_user,update_user
from auth.schemas import UserCreate
from auth.hashing import ver_pass


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
def test_create_user_duplicate_email(db):
    user_data=UserCreate(
        name="Panos",
        email="Panos@gmail.com",
        password="Panos"
        
    )
    
    created=create_user(db,user_data)
    with pytest.raises(HTTPException) as exc_info:
        created=create_user(db,user_data)
    assert exc_info.value.status_code==409



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

def test_get_user_success(db):
    user_data=UserCreate(
    name="Panos",
    email="Panos@gmail.com",
    password="Panos"
        
    )
    created=create_user(db,user_data)
    get_user=get_user_or_404(db,created.id)
    assert get_user.id==created.id
    assert get_user.name==created.name
    assert get_user.email==created.email
    assert ver_pass("Panos",created.hashed_password)

def test_update_user(db):
    user_data=UserCreate(
    name="Panos",
    email="Panos@gmail.com",
    password="Panos"        
    )
    created=create_user(db,user_data)
    new_user_data=UserCreate(
    name="kalos",
    email="Panosss@gmail.com",
    password="Panos"        
    )
    updated_user=update_user(db,created.id,new_user_data)
    assert created.id==updated_user.id
    assert new_user_data.name==updated_user.name
    assert new_user_data.email==updated_user.email
    assert ver_pass("Panos",updated_user.hashed_password)
    
