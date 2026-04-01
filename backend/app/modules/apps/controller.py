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
    service = AppService(AppRepository(db))
    return await service.list_apps()

@router.post("/", response_model=AppResponse)
async def create_app(data: AppCreate, db: AsyncSession = Depends(get_db)):
    service = AppService(AppRepository(db))
    return await service.create_app(data.model_dict())