from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

# Imports necessários para resolver o NameError
from .service import AuthService
from .repository import AuthRepository
from .schemas import LoginRequest, TokenResponse
from app.modules.users.repository import UserRepository 
from app.core.security import create_access_token

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    # Agora o Python sabe quem são AuthRepository e UserRepository
    auth_repo = AuthRepository(db)
    user_repo = UserRepository(db)
    service = AuthService(auth_repo, user_repo)
    
    user = await service.authenticate(data.username, data.password)
    
    # Geração dos tokens
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
    auth_repo = AuthRepository(db)
    await auth_repo.delete_refresh_token(refresh_token)
    return {"detail": "Deslogado com sucesso"}