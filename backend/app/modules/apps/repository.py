"""
Repository layer for application data access.

This module provides the AppRepository class for managing application records
in the database, including retrieval and creation operations.

Operations:
    - Get all active applications
    - Create new applications
"""

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import AppModel

class AppRepository:
    """
    Repository for application-related database operations.

    Handles CRUD operations for applications using SQLAlchemy async sessions.
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize the repository with a database session.

        Args:
            db (AsyncSession): The async database session.
        """
        self.db = db

    async def get_all(self):
        """
        Retrieve all active applications.

        Returns:
            list[AppModel]: List of active application instances.
        """
        result = await self.db.execute(select(AppModel).filter(AppModel.is_active == True))
        return result.scalars().all()

    async def create(self, app_data: dict):
        """
        Create a new application in the database.

        Args:
            app_data (dict): Dictionary of application data.

        Returns:
            AppModel: The created application instance.
        """
        db_app = AppModel(**app_data)
        self.db.add(db_app)
        await self.db.commit()
        await self.db.refresh(db_app)
        return db_app