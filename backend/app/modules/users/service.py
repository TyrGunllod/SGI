"""
User service layer for business logic.

This module provides the UserService class that handles user management operations,
including user creation with password hashing and validation.

Operations:
    - Retrieve all users
    - Create new users with secure password hashing
"""

from .repository import UserRepository
from .schemas import UserCreate
from .models import User  # Import the User model
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    """
    Service for user-related business logic.

    Manages user operations like creation and retrieval with proper validation.
    """

    def __init__(self, repository: UserRepository):
        """
        Initialize the service with a user repository.

        Args:
            repository (UserRepository): The user data repository.
        """
        self.repository = repository

    async def get_all_users(self):
        """
        Retrieve all active users.

        Returns:
            list[User]: List of all active users.
        """
        return await self.repository.get_all()

    async def create_user(self, user_data: UserCreate):
        """
        Create a new user with hashed password.

        Validates for duplicate usernames and hashes the password before saving.

        Args:
            user_data (UserCreate): The user creation data.

        Returns:
            User: The created user instance.

        Raises:
            Exception: If username already exists.
        """
        # Check for duplicate username
        existing = await self.repository.get_by_username(user_data.username)
        if existing:
            raise Exception("Username already exists")

        # Hash the password
        hashed_pwd = pwd_context.hash(user_data.password)

        # Create user model instance
        user_model = User(
            username=user_data.username,
            hashed_password=hashed_pwd,
            full_name=user_data.full_name,
            is_active=user_data.is_active,
            is_admin=user_data.is_admin,
        )

        return await self.repository.create(user_model)
