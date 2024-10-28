from typing import Annotated

from app.db import get_user_by_email, user_collection
from app.dependencies import create_access_token
from app.models import User
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

auth_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@auth_router.post("/register")
async def register(user: User):
    """
    Registers a new user by creating an account with a hashed password.
    
    Args:
        user (User): The user object containing details such as email, username, and password.
    
    Raises:
        HTTPException: If an account with the same email already exists.
    
    Returns:
        Dict: A success message confirming user creation.
    """
    try:
        existing_user = await get_user_by_email(user.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = pwd_context.hash(user.password)
        user.password = hashed_password
        await user_collection.insert_one(user.dict())
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registering user: {e}")

@auth_router.post("/token")
async def login(login_request:Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Authenticates a user and generates an access token for future API requests.
    
    Args:
        login_request (LoginRequest): Login credentials including username and password.
    
    Raises:
        HTTPException: If the username or password is invalid, or if authentication fails.
    
    Returns:
        Dict: An access token and the token type ("bearer") for authorized access.
    """
    try:
        print("hello")
        user = await user_collection.find_one({"username": login_request.username.lower()})
        print(user)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = create_access_token(data={"sub": str(user['_id']), "role": user['role']})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error logging in: {e}")
