"""
Pydantic schemas for user data validation and serialization.

This module defines the data models for user creation, updates, and responses
in the users API, ensuring data integrity and type safety.

Schemas:
    - UserBase: Common user fields
    - UserCreate: For creating new users (includes password)
    - UserResponse: For API responses (includes ID)
"""

from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class UserBase(BaseModel):
    """
    Base schema for user data.

    Contains common fields used in user operations.
    """
    username: str
    full_name: Optional[str] = None
    is_active: bool = True
    is_admin: bool = False

class UserCreate(UserBase):
    """
    Schema for creating new users.

    Extends UserBase with password field required for registration.
    """
    password: str

class UserResponse(UserBase):
    """
    Schema for user data in API responses.

    Includes the user ID and configures Pydantic to work with SQLAlchemy models.
    """
    id: UUID

    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy models
