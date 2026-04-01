"""
Repository layer for authentication data access.

This module provides the AuthRepository class for managing refresh tokens
in the database, including saving, retrieving, and deleting tokens.

Operations:
    - Save new refresh tokens
    - Retrieve tokens by string
    - Delete expired or invalid tokens
"""

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import RefreshToken
from datetime import datetime

class AuthRepository:
    """
    Repository for authentication-related database operations.

    Handles CRUD operations for refresh tokens using SQLAlchemy async sessions.
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize the repository with a database session.

        Args:
            db (AsyncSession): The async database session.
        """
        self.db = db

    async def save_refresh_token(self, user_id, token: str, expires_at: datetime):
        """
        Save a new refresh token to the database.

        Args:
            user_id: The ID of the user owning the token.
            token (str): The refresh token string.
            expires_at (datetime): The expiration timestamp.

        Returns:
            RefreshToken: The saved token instance.
        """
        db_token = RefreshToken(user_id=user_id, token=token, expires_at=expires_at)
        self.db.add(db_token)
        await self.db.commit()
        return db_token

    async def get_refresh_token(self, token: str):
        """
        Retrieve a refresh token by its string value.

        Args:
            token (str): The refresh token string.

        Returns:
            RefreshToken or None: The token instance if found, else None.
        """
        result = await self.db.execute(select(RefreshToken).filter(RefreshToken.token == token))
        return result.scalars().first()

    async def delete_refresh_token(self, token: str):
        """
        Delete a refresh token from the database.

        Args:
            token (str): The refresh token string to delete.
        """
        db_token = await self.get_refresh_token(token)
        if db_token:
            await self.db.delete(db_token)
            await self.db.commit()