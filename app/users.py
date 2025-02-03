from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.models import User
from app.database import get_db

router = APIRouter()


@router.post('/')
async def create_user(email: str, password: str, full_name: str, is_admin: bool = False,
                      db: AsyncSession = Depends(get_db)):
    return await crud.create_user(db, email, password, full_name, is_admin)


@router.get("/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_id(db, user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True, "data": db_user}


@router.put("/{user_id}")
async def update_user(user_id: int, full_name: str, is_admin: bool, db: AsyncSession = Depends(get_db)):
    return await crud.update_user(db, user_id, full_name, is_admin)


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_user(db, user_id)
