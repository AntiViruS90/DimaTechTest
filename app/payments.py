from fastapi import APIRouter, Depends, HTTPException
import hashlib
import os
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Payment, Account

router = APIRouter()

SECRET_KEY = os.getenv('SECRET_KEY')


def verify_signature(data: dict, signature: str) -> bool:
    data_str = f"{data['account_id']}{data['amount']}{data['transaction_id']}{data['user_id']}{SECRET_KEY}"
    expected_signature = hashlib.sha256(data_str.encode()).hexdigest()
    return expected_signature == signature


@router.post("/webhook")
async def handle_webhook(data: dict, db: AsyncSession = Depends(get_db)):
    if not verify_signature(data, data['signature']):
        raise HTTPException(status_code=400, detail='Invalid signature')

    transaction_exists = await db.execute(
        Payment.__table__.select().where(Payment.transaction_id == data['transaction_id'])
    )
    if transaction_exists.scalars().first():
        raise HTTPException(status_code=400, detail='Transaction already processed')

    account = await db.execute(
        Account.__table__.select().where(Account.id == data['account_id'])
    )
    account = account.scalars().first()

    if not account:
        account = Account(id=data['account_id'], user_id=data['user_id'], balance=0.0)
        db.add(account)

    account.balance += data['amount']
    db.add(Payment(**data))
    await db.commit()

    return {"success": True}
