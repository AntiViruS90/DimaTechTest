from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.models import Account
from app.database import get_db

router = APIRouter()


@router.post("/")
async def create_account(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.create_account(db, user_id)


@router.get("/{user_id}")
async def get_accounts(user_id: int, db: AsyncSession = Depends(get_db)):
    accounts = await crud.get_account_by_user_id(db, user_id)

    if not accounts:
        raise HTTPException(status_code=404, detail="No accounts found for this user")
    return {"success": True, "data": accounts}
