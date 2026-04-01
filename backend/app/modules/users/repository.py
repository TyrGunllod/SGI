from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_username(self, username: str):
        result = await self.db.execute(select(User).filter(User.username == username))
        return result.scalars().first()

    async def create(self, user: User):
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user