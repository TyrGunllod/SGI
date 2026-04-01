"""
Application models for the apps module.

This module defines the SQLAlchemy model for applications in the system,
representing the apps that users can access.

Table: applications

Fields:
    - id: UUID primary key
    - name: Display name of the app
    - slug: URL-friendly unique identifier
    - description: Brief description
    - icon: Icon name (e.g., from Lucide)
    - path: URL path for the app
    - is_active: Active status
"""

from sqlalchemy import Column, String, Boolean, text
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid

class AppModel(Base):
    """
    SQLAlchemy model representing an application in the system.

    Inherits from Base for automatic timestamps (created_at, updated_at).
    """

    __tablename__ = "applications"

    # UUID primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Human-readable name of the application
    name = Column(String, nullable=False)
    # Unique slug for URL and identification
    slug = Column(String, unique=True, nullable=False)
    # Optional description of the app's purpose
    description = Column(String, nullable=True)
    # Icon name from Lucide icon set
    icon = Column(String, default="Package")
    # URL path for accessing the app
    path = Column(String, unique=True, nullable=True)
    # Active status flag
    is_active = Column(Boolean, default=True)