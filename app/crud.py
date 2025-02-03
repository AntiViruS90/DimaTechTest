from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from app.models import User, Account
from app.auth import hash_password


async def create_user(db: AsyncSession, email: str, password: str, full_name: str,  is_admin: bool = False):
    db_user = User(email=email, hashed_password=hash_password(password), full_name=full_name, is_admin=is_admin)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()


async def create_account(db: AsyncSession, user_id: int):
    db_account = Account(user_id=user_id)
    db.add(db_account)
    await db.commit()
    await db.refresh(db_account)
    return db_account


async def get_account_by_user_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(Account).filter(Account.user_id == user_id))
    return result.scalars().first()


async def update_user(db: AsyncSession, user_id: int, full_name: str, is_admin: bool):
    db_user = await get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')

    db_user.full_name = full_name
    db_user.is_admin = is_admin
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: int):
    db_user = await get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')

    await db.delete(db_user)
    await db.commit()
    return {"succes": True}
