"""
Users controller for API endpoints.

This module defines the FastAPI router and endpoints for user management,
including listing users and creating new users.

Endpoints:
    - GET /: List all active users
    - POST /: Create a new user
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from .service import UserService
from .repository import UserRepository
from .models import User
from .schemas import UserCreate, UserResponse

router = APIRouter()

@router.get("/", response_model=list[UserResponse])
async def list_users(db: AsyncSession = Depends(get_db)):
    """
    Retrieve a list of all active users.

    Args:
        db (AsyncSession): Database session dependency.

    Returns:
        list[UserResponse]: List of user data.
    """
    service = UserService(UserRepository(db))
    return await service.get_all_users()

@router.post("/", response_model=UserResponse)
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new user.

    Validates data, hashes password, and saves the user.

    Args:
        data (UserCreate): User creation data.
        db (AsyncSession): Database session dependency.

    Returns:
        UserResponse: The created user data.

    Raises:
        HTTPException: 400 for validation errors like duplicate username.
    """
    service = UserService(UserRepository(db))
    try:
        user = await service.create_user(data)
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
