"""
Authentication models for token management.

This module defines the SQLAlchemy model for refresh tokens used in JWT authentication.
Refresh tokens allow obtaining new access tokens without re-authentication.

Table: refresh_tokens

Fields:
    - id: UUID primary key
    - user_id: Foreign key to users table
    - token: Unique refresh token string
    - expires_at: Expiration timestamp
    - created_at/updated_at: Automatic timestamps
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid

class RefreshToken(Base):
    """
    SQLAlchemy model for storing refresh tokens.

    Refresh tokens are used to generate new access tokens and have longer expiration times.
    """

    __tablename__ = "refresh_tokens"

    # UUID primary key for the token
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Foreign key linking to the user who owns the token
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # The actual refresh token string, must be unique
    token = Column(String, unique=True, index=True, nullable=False)
    # Expiration timestamp for the token
    expires_at = Column(DateTime(timezone=True), nullable=False)
    # Creation timestamp
    created_at = Column(DateTime(timezone=True), server_default=text("now()"))
    # Update timestamp, updated on changes
    updated_at = Column(DateTime(timezone=True), server_default=text("now()"), onupdate=text("now()"))