from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import AppModel

class AppRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(select(AppModel).filter(AppModel.is_active == True))
        return result.scalars().all()

    async def create(self, app_data: dict):
        db_app = AppModel(**app_data)
        self.db.add(db_app)
        await self.db.commit()
        await self.db.refresh(db_app)
        return db_app