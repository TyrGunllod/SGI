"""
Repository layer for user data access.

This module provides the UserRepository class for managing user records
in the database, including retrieval, creation, and filtering operations.

Operations:
    - Get all active users
    - Get user by username
    - Get user by ID
    - Create new user
"""

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User

class UserRepository:
    """
    Repository for user-related database operations.

    Handles CRUD operations for users using SQLAlchemy async sessions.
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
        Retrieve all active users.

        Returns:
            list[User]: List of active user instances.
        """
        result = await self.db.execute(select(User).filter(User.is_active == True))
        return result.scalars().all()

    async def get_by_username(self, username: str):
        """
        Retrieve a user by their username.

        Args:
            username (str): The username to search for.

        Returns:
            User or None: The user instance if found, else None.
        """
        result = await self.db.execute(select(User).filter(User.username == username))
        return result.scalars().first()

    async def get_by_id(self, user_id):
        """
        Retrieve a user by their ID.

        Args:
            user_id: The UUID of the user.

        Returns:
            User or None: The user instance if found, else None.
        """
        result = await self.db.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()

    async def create(self, user: User):
        """
        Create a new user in the database.

        Args:
            user (User): The user instance to save.

        Returns:
            User: The saved user instance with refreshed data.
        """
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user