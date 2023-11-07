import uuid
from fastapi import APIRouter, HTTPException
from classes.schema_dto import User
from firebase_admin import auth
from pydantic import BaseModel

router = APIRouter(
    tags=["UserAccounts"]
)

user_accounts = []

@router.post('/user-accounts', status_code=201)
async def create_user_account(user: User):
    new_user = User(id=str(uuid.uuid4()), email=user.email, password=user.password)
    user_accounts.append(new_user)
    return new_user

@router.get('/user-accounts')
async def get_all_user_accounts():
    return user_accounts

@router.get('/user-accounts/{user_id}')
async def get_user_account(user_id: str):
    for user in user_accounts:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User account not found")

@router.patch('/user-accounts/{user_id}')
async def update_user_account(user_id: str, updated_user: User):
    for user in user_accounts:
        if user.id == user_id:
            user.email = updated_user.email
            user.password = updated_user.password
            return user
    raise HTTPException(status_code=404, detail="User account not found")

@router.delete('/user-accounts/{user_id}', status_code=204)
async def delete_user_account(user_id: str):
    for user in user_accounts:
        if user.id == user_id:
            user_accounts.remove(user)
            return
    raise HTTPException(status_code=404, detail="User account not found")
