"""
User models for the users module.

This module defines the SQLAlchemy model for users in the system,
including authentication fields and user attributes.

Table: users

Fields:
    - id: UUID primary key
    - username: Unique username
    - hashed_password: Secure password hash
    - full_name: User's full name
    - is_active: Account active status
    - is_admin: Administrative privileges
"""

from sqlalchemy import Column, String, Boolean, UUID
import uuid
from app.database import Base

class User(Base):
    """
    SQLAlchemy model representing a user in the system.

    Inherits from Base for automatic timestamps (created_at, updated_at).
    """

    __tablename__ = "users"

    # UUID primary key for the user
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Unique username for login
    username = Column(String, unique=True, index=True, nullable=False)
    # Hashed password for security
    hashed_password = Column(String, nullable=False)
    # Full name of the user
    full_name = Column(String)
    # Flag for active account status
    is_active = Column(Boolean, default=True)
    # Flag for administrative privileges
    is_admin = Column(Boolean, default=False)