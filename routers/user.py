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
async def read_users():
    await db.connect()
    # await db.create_table()
    data = await db.all()
    await db.close()
    return BaseResponse(data=data)

@router.get("/{user_id}", response_model=BaseResponse)
async def read_user(user_id: int):
    await db.connect()
    data = await db.get_user_by_id(id=user_id)
    await db.close()
    return BaseResponse(data=data)

@router.post("/create",response_model=BaseResponse)
async def create_user(user: User):
    await db.connect()
    data  = await db.add(full_name=user.full_name,username=user.username,email=user.email,password=user.password)
    await db.close()
    return  BaseResponse(data=data)

@router.put("/update/{user_id}", response_model=BaseResponse)
async def update_user(user: User, user_id: int):
    await db.connect()
    affected_rows = await db.update(id=user_id, full_name=user.full_name,username=user.username ,email=user.email, password=user.password)
    await db.close()
    
    if affected_rows > 0:
        return BaseResponse(data={"message": "User updated successfully"})
    else:
        return BaseResponse(status=False, errors=[{"message": "User not found or no changes made"}])


@router.delete("/delete/{user_id}")
async def delete_user(user_id: int):
    await db.connect()
    data = await db.delete(user_id=user_id)
    await db.close()
    return BaseResponse(data=data)

