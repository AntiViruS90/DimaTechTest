from fastapi import APIRouter

from .users import router as users_router
from .accounts import router as accounts_router
from .payments import router as payments_router

router = APIRouter()

router.include_router(users_router, prefix='/api/v1/users')
router.include_router(accounts_router, prefix='/api/v1/accounts')
router.include_router(payments_router, prefix='/api/v1/payments')
