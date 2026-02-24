from fastapi import FastAPI
from app.routers import users as user_router
from app.routers import categories as category_router
from app.routers import auth as auth_router
from app.routers import wallets as wallet_router
from app.routers import transaction as transaction_router
from app.routers import analytics as analytics_router

from app.models.categories import Category
from app.models.transaction import Transaction
from app.models.users import User
from app.models.wallets import Wallet


app = FastAPI()

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(category_router.router)  
app.include_router(wallet_router.router)
app.include_router(transaction_router.router)
app.include_router(analytics_router.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)