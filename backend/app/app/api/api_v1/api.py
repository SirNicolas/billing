from fastapi import APIRouter

from app.api.api_v1.resources import auth, user, wallet, transaction

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(wallet.router, prefix="/wallet", tags=["wallet"])
api_router.include_router(transaction.router, prefix="/transaction", tags=["transaction"])
