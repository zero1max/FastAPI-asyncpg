from fastapi import APIRouter
import asyncio
from models import User,BaseResponse
from db import Database
from config import DATABASE_URL

db = Database(DATABASE_URL)

router = APIRouter(
    prefix= "/users"
)


@router.get("")
async def read_users(users):
    ...

@router.post("",response_model=BaseResponse)
async def create_user(user: User):
    await db.connect()
    data  = await db.add(full_name=user.full_name,username=user.username,email=user.email,password=user.password)
    await db.close()
    return  BaseResponse(data=data)

@router.put("")
async def update_user(user_id: int):
    ...

@router.delete("")
async def delete_user(user_id: int):
    ...

