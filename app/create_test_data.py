import asyncio
from app import crud
from app.database import SessionLocal
from app.models import Payment


async def create_test_data():
    async with SessionLocal() as db:
        admin = await crud.create_user(
            db,
            email="admin@example.com",
            password="admin123",
            full_name="Admin",
            is_admin=True
        )
        user = await crud.create_user(
            db,
            email="user@example.com",
            password="user123",
            full_name="User",
            is_admin=False
        )
        user_2 = await crud.create_user(
            db,
            email="user_2@example.com",
            password="user_2123",
            full_name="User_2",
            is_admin=False
        )

        account = await crud.create_account(db, user.id)
        test_payment = Payment(
            transaction_id="test_txn_123",
            account_id=account.id,
            user_id=user.id,
            amount=100.0
        )
        db.add(test_payment)
        await db.commit()


if __name__ == '__main__':
    asyncio.run(create_test_data())
