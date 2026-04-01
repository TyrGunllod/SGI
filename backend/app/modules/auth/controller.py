"""
Authentication controller for API endpoints.

This module defines the FastAPI router and endpoints for user authentication,
including login, logout, and token refresh operations.

Endpoints:
    - POST /login: Authenticate user and return tokens
    - POST /logout: Invalidate refresh token
    - POST /refresh: Refresh access token using refresh token
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

# Imports for authentication components
from .service import AuthService
from .repository import AuthRepository
from .schemas import LoginRequest, TokenResponse, RefreshTokenRequest
from app.modules.users.repository import UserRepository
from app.core.security import create_access_token

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    """
    Authenticate a user and return JWT tokens.

    Validates username/password, generates access and refresh tokens,
    and returns user summary.

    Args:
        data (LoginRequest): Login credentials.
        db (AsyncSession): Database session.

    Returns:
        TokenResponse: Access token, refresh token, and user info.
    """
    # Initialize repositories and service
    auth_repo = AuthRepository(db)
    user_repo = UserRepository(db)
    service = AuthService(auth_repo, user_repo)
    
    # Authenticate user
    user = await service.authenticate(data.username, data.password)
    
    # Generate tokens
    access_token = create_access_token(user.id)
    refresh_token = await service.create_refresh_token(user.id)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "username": user.username, 
            "is_admin": user.is_admin
        }
    }

@router.post("/logout")
async def logout(refresh_token: str, db: AsyncSession = Depends(get_db)):
    """
    Logout user by invalidating their refresh token.

    Args:
        refresh_token (str): The refresh token to invalidate.
        db (AsyncSession): Database session.

    Returns:
        dict: Success message.
    """
    auth_repo = AuthRepository(db)
    await auth_repo.delete_refresh_token(refresh_token)
    return {"detail": "Deslogado com sucesso"}

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(data: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    """
    Refresh access token using a valid refresh token.

    Generates new access token and returns updated token response.

    Args:
        data (RefreshTokenRequest): Contains the refresh token.
        db (AsyncSession): Database session.

    Returns:
        TokenResponse: New access token with existing refresh token and user info.

    Raises:
        HTTPException: If user is not found.
    """
    refresh_token = data.refresh_token
    auth_repo = AuthRepository(db)
    user_repo = UserRepository(db)
    service = AuthService(auth_repo, user_repo)

    # Generate new access token
    access_token = await service.refresh_access_token(refresh_token)
    db_token = await auth_repo.get_refresh_token(refresh_token)
    user = await user_repo.get_by_id(db_token.user_id)

    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "username": user.username,
            "is_admin": user.is_admin
        }
    }