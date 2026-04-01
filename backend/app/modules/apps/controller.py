"""
Apps controller for API endpoints.

This module defines the FastAPI router and endpoints for application management,
including listing applications and creating new ones.

Endpoints:
    - GET /: List all active applications
    - POST /: Create a new application
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from .schemas import AppResponse, AppCreate
from .service import AppService
from .repository import AppRepository
from typing import List

router = APIRouter()

@router.get("/", response_model=List[AppResponse])
async def list_apps(db: AsyncSession = Depends(get_db)):
    """
    Retrieve a list of all active applications.

    Args:
        db (AsyncSession): Database session dependency.

    Returns:
        List[AppResponse]: List of application data.
    """
    service = AppService(AppRepository(db))
    return await service.list_apps()

@router.post("/", response_model=AppResponse)
async def create_app(data: AppCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new application.

    Args:
        data (AppCreate): Application creation data.
        db (AsyncSession): Database session dependency.

    Returns:
        AppResponse: The created application data.
    """
    service = AppService(AppRepository(db))
    return await service.create_app(data.model_dict())