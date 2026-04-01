"""
User model for the internal user management.

This module defines the SQLAlchemy model for users in the system,
including fields for authentication and basic user information.

Table: usuarios

Fields:
    - id: Primary key
    - username: Unique username for login
    - senha_hash: Hashed password
    - nome: Full name
    - ativo: Active status
    - criado_em: Creation timestamp
"""

from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text
from app.database import Base

class User(Base):
    """
    SQLAlchemy model representing a user in the system.

    Inherits from Base for automatic timestamps (created_at, updated_at).
    """

    __tablename__ = "usuarios"

    # Primary key for the user
    id = Column(Integer, primary_key=True, index=True)

    # Unique username for authentication
    username = Column(String, unique=True, nullable=False)

    # Hashed password for security
    senha_hash = Column(String, nullable=False)

    # Full name of the user
    nome = Column(String)

    # Flag to indicate if the user account is active
    ativo = Column(Boolean, default=True)

    # Timestamp for when the user was created
    criado_em = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))