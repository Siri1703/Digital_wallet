# app/main.py
from app.db import create_collections
from app.routes.admin_routes import admin_router
from app.routes.authentication_routes import auth_router
from app.routes.user_routes import user_router
from fastapi import FastAPI

app = FastAPI()
# Include routers
app.include_router(user_router, prefix="/wallets", tags=["User Wallet"])
app.include_router(admin_router, prefix="/admin", tags=["Admin Dashboard"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Digital Wallet API"}


@app.on_event("startup")
async def startup_event():
    await create_collections()
    print("Database setup completed.")
