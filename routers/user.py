from fastapi import APIRouter
import asyncio
from models import User, BaseResponse
from db import Database
from config import DATABASE_URL
from services import make_password

db = Database(DATABASE_URL)

router = APIRouter(
    prefix="/users"
)


@router.get("", response_model=BaseResponse)
async def read_users():
    await db.connect()
    users = await db.all()
    await db.close()
    return BaseResponse(data=users)


@router.post("", response_model=BaseResponse)
async def create_user(user: User):
    await db.connect()
    data = await db.add(full_name=user.full_name, username=user.username, email=user.email,
                        password=make_password(user.password))
    await db.close()
    return BaseResponse(data=data)


@router.put("", response_model=BaseResponse)
async def update_user(user: User, user_id: int, ):
    await db.connect()
    users = await db.update(user_id, user.full_name, user.username, user.email, user.password)
    await db.close()
    return BaseResponse(data=users)


@router.delete("", response_model=BaseResponse)
async def delete_user(user_id: int):
    await db.connect()
    users = await db.delete(user_id)
    await db.close()
    return BaseResponse(data=users)