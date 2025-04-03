from fastapi import APIRouter, HTTPException
import asyncio
from models import User, BaseResponse
from db import Database, UserAlreadyExistsError, DatabaseError
from config import DATABASE_URL
from services.password import hash_password
from typing import Optional

db = Database(DATABASE_URL)

router = APIRouter(
    prefix="/users"
)

@router.get("", response_model=BaseResponse)
async def read_users():
    try:
        await db.connect()
        users = await db.all()
        await db.close()
        return BaseResponse(data=users)
    except Exception as e:
        return BaseResponse(status=False, errors=[{"message": str(e)}])

@router.get("/{user_id}", response_model=BaseResponse)
async def read_user(user_id: int):
    try:
        await db.connect()
        user = await db.get_user_by_id(user_id)
        await db.close()
        
        if not user:
            return BaseResponse(status=False, errors=[{"message": "User not found"}])
            
        return BaseResponse(data=user)
    except Exception as e:
        return BaseResponse(status=False, errors=[{"message": str(e)}])

@router.post("", response_model=BaseResponse)
async def create_user(user: User):
    try:
        # Hash the password before storing
        hashed_password = hash_password(user.password)
        
        await db.connect()
        data = await db.add(
            full_name=user.full_name, 
            username=user.username, 
            email=user.email,
            password=hashed_password.decode('utf-8')  # Convert bytes to string for storage
        )
        await db.close()
        return BaseResponse(data=data)
    except UserAlreadyExistsError as e:
        return BaseResponse(status=False, errors=[{"message": str(e)}])
    except Exception as e:
        return BaseResponse(status=False, errors=[{"message": str(e)}])

@router.put("/{user_id}", response_model=BaseResponse)
async def update_user(user: User, user_id: int):
    try:
        # Hash the password before storing
        hashed_password = hash_password(user.password)
        
        await db.connect()
        success = await db.update(
            id=user_id,
            full_name=user.full_name, 
            username=user.username, 
            email=user.email,
            password=hashed_password.decode('utf-8')  # Convert bytes to string for storage
        )
        await db.close()
        
        if success:
            return BaseResponse(data={"message": "User updated successfully"})
        else:
            return BaseResponse(status=False, errors=[{"message": "User not found"}])
    except UserAlreadyExistsError as e:
        return BaseResponse(status=False, errors=[{"message": str(e)}])
    except Exception as e:
        return BaseResponse(status=False, errors=[{"message": str(e)}])

@router.delete("/{user_id}", response_model=BaseResponse)
async def delete_user(user_id: int):
    try:
        await db.connect()
        success = await db.delete(user_id=user_id)
        await db.close()
        
        if success:
            return BaseResponse(data={"message": "User deleted successfully"})
        else:
            return BaseResponse(status=False, errors=[{"message": "User not found"}])
    except Exception as e:
        return BaseResponse(status=False, errors=[{"message": str(e)}])