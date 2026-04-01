from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import RefreshToken
from datetime import datetime

class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_refresh_token(self, user_id, token: str, expires_at: datetime):
        db_token = RefreshToken(user_id=user_id, token=token, expires_at=expires_at)
        self.db.add(db_token)
        await self.db.commit()
        return db_token

    async def get_refresh_token(self, token: str):
        result = await self.db.execute(select(RefreshToken).filter(RefreshToken.token == token))
        return result.scalars().first()

    async def delete_refresh_token(self, token: str):
        db_token = await self.get_refresh_token(token)
        if db_token:
            await self.db.delete(db_token)
            await self.db.commit()