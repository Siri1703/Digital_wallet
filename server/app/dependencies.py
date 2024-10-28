from datetime import datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from .db import get_user_by_email
from .models import User

# OAuth2 password bearer for token retrieval
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Secret key for encoding/decoding JWT
SECRET_KEY = "secret"  # Change this to a secure key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Retrieves the current authenticated user from the JWT token.

    Args:
        token (str): The JWT token used for user authentication, extracted through dependency injection.

    Raises:
        HTTPException: If the token is invalid, expired, or the user cannot be found.

    Returns:
        User: The user object associated with the token's "sub" claim.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        print(user_id)
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

        user = await get_user_by_email(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    except Exception as ex:
        # Log the error for debugging purposes (you can use logging module)
        print(f"Error retrieving current user: {ex}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

def role_required(required_role: str):
    """
    Creates a role-based dependency that checks if a user has the specified role.

    Args:
        required_role (str): The required role to access a particular route.

    Raises:
        HTTPException: If the user's role does not match the required role.

    Returns:
        function: A dependency that can be used in routes to enforce role-based access control.
    """
    async def role_checker(user: User = Depends(get_current_user)):
        if user.role != required_role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
        return user
    return role_checker

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Generates a JWT token for a user with an optional expiration time.

    Args:
        data (dict): The data payload to encode in the token.
        expires_delta (timedelta, optional): The time duration until the token expires. Defaults to ACCESS_TOKEN_EXPIRE_MINUTES.

    Returns:
        str: The generated JWT token.
    """
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as ex:
        # Log the error for debugging purposes (you can use logging module)
        print(f"Error creating access token: {ex}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not create access token")
