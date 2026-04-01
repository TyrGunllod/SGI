from datetime import datetime, timedelta, timezone
import secrets
from fastapi import HTTPException, status
from app.core.security import verify_password, create_access_token
from .repository import AuthRepository
from app.modules.users.repository import UserRepository

class AuthService:
    def __init__(self, auth_repo: AuthRepository, user_repo: UserRepository):
        self.auth_repo = auth_repo
        self.user_repo = user_repo

    async def authenticate(self, username, password):
        user = await self.user_repo.get_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
        
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Usuário desativado")
            
        return user

    async def create_refresh_token(self, user_id):
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        await self.auth_repo.save_refresh_token(user_id, token, expires_at)
        return token

    async def refresh_access_token(self, refresh_token: str):
        db_token = await self.auth_repo.get_refresh_token(refresh_token)
        if not db_token or db_token.expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Refresh token expirado ou inválido")
            
        return create_access_token(db_token.user_id)