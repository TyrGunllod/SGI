"""
Authentication service layer for business logic.

This module provides the AuthService class that handles user authentication,
password verification, refresh token creation, and access token refreshing.

Operations:
    - Authenticate users with username/password
    - Create refresh tokens for persistent sessions
    - Refresh access tokens using valid refresh tokens
"""

from datetime import datetime, timedelta, timezone
import secrets
from fastapi import HTTPException, status
from app.core.security import verify_password, create_access_token
from .repository import AuthRepository
from app.modules.users.repository import UserRepository

class AuthService:
    """
    Service for authentication-related business logic.

    Manages user login, token generation, and session handling.
    """

    def __init__(self, auth_repo: AuthRepository, user_repo: UserRepository):
        """
        Initialize the service with required repositories.

        Args:
            auth_repo (AuthRepository): Repository for auth data.
            user_repo (UserRepository): Repository for user data.
        """
        self.auth_repo = auth_repo
        self.user_repo = user_repo

    async def authenticate(self, username, password):
        """
        Authenticate a user with username and password.

        Verifies credentials and checks if the user is active.

        Args:
            username (str): The user's username.
            password (str): The user's password.

        Returns:
            User: The authenticated user object.

        Raises:
            HTTPException: 401 for invalid credentials, 400 for inactive user.
        """
        user = await self.user_repo.get_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
        
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Usuário desativado")
            
        return user

    async def create_refresh_token(self, user_id):
        """
        Create a new refresh token for the user.

        Generates a secure random token with 7-day expiration.

        Args:
            user_id: The ID of the user.

        Returns:
            str: The generated refresh token.
        """
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        await self.auth_repo.save_refresh_token(user_id, token, expires_at)
        return token

    async def refresh_access_token(self, refresh_token: str):
        """
        Refresh an access token using a valid refresh token.

        Validates the refresh token and generates a new access token.

        Args:
            refresh_token (str): The refresh token string.

        Returns:
            str: A new access token.

        Raises:
            HTTPException: 401 for expired or invalid refresh token.
        """
        db_token = await self.auth_repo.get_refresh_token(refresh_token)
        if not db_token or db_token.expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Refresh token expirado ou inválido")
            
        return create_access_token(db_token.user_id)