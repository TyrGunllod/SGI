"""
Dependencies module for authentication and user retrieval.

This module provides FastAPI dependencies for handling OAuth2 token-based authentication,
decoding JWT tokens, and extracting the current user's ID from the token payload.

Dependencies:
    - fastapi for HTTP exceptions and dependency injection
    - jose for JWT token handling
    - app.core.security for secret key and algorithm constants
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from app.core.security import SECRET_KEY, ALGORITHM

# OAuth2 scheme for token-based authentication, pointing to the login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependency to retrieve the current authenticated user from the JWT token.

    Decodes the token, extracts the user ID from the 'sub' claim, and validates it.
    Raises HTTP 401 exceptions for invalid or missing tokens.

    Args:
        token (str): The JWT access token from the Authorization header.

    Returns:
        str: The user ID extracted from the token.

    Raises:
        HTTPException: If the token is invalid or credentials are incorrect.
    """
    try:
        # Decode the JWT token using the secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Extract user ID from the subject claim
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return user_id
    except Exception:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")