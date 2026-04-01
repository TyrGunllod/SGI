"""
Permission models for access control.

This module defines the SQLAlchemy models for applications, pages, and permissions
in the system, enabling fine-grained access control.

Tables:
    - applications: System applications
    - pages: Pages within applications
    - permissions: User permissions for apps/pages

Relationships:
    - Application has many Pages and Permissions
    - Page belongs to Application and has Permissions
    - Permission links User, Application, and optionally Page
"""

from sqlalchemy import Column, Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.database import Base

class Application(Base):
    """
    SQLAlchemy model for system applications.

    Represents apps that users can access, with metadata and relationships.
    """

    __tablename__ = "applications"

    # UUID primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Application name
    name = Column(String(100), unique=True, nullable=False)
    # URL-friendly slug
    slug = Column(String(100), unique=True, nullable=False)
    # Description of the application
    description = Column(Text)
    # Icon identifier
    icon = Column(String(50))
    # Active status
    is_active = Column(Boolean, default=True)

    # Relationships
    pages = relationship("Page", back_populates="application")
    permissions = relationship("Permission", back_populates="application")

class Page(Base):
    """
    SQLAlchemy model for application pages.

    Represents individual pages within applications.
    """

    __tablename__ = "pages"

    # UUID primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Foreign key to application
    app_id = Column(UUID(as_uuid=True), ForeignKey("applications.id", ondelete="CASCADE"), nullable=False)
    # Page title
    title = Column(String(100), nullable=False)
    # URL path
    path = Column(String(255), nullable=False)
    # Whether the page is external
    is_external = Column(Boolean, default=False)
    # HTML content for the page
    html_content = Column(Text)

    # Relationships
    application = relationship("Application", back_populates="pages")
    permissions = relationship("Permission", back_populates="page")

class Permission(Base):
    """
    SQLAlchemy model for user permissions.

    Defines what actions a user can perform on applications and pages.
    """

    __tablename__ = "permissions"

    # UUID primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Foreign key to user
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # Foreign key to application
    app_id = Column(UUID(as_uuid=True), ForeignKey("applications.id", ondelete="CASCADE"), nullable=False)
    # Optional foreign key to page
    page_id = Column(UUID(as_uuid=True), ForeignKey("pages.id", ondelete="CASCADE"), nullable=True)
    # Permission flags
    can_view = Column(Boolean, default=True)
    can_edit = Column(Boolean, default=False)
    can_delete = Column(Boolean, default=False)

    # Relationships
    application = relationship("Application", back_populates="permissions")
    page = relationship("Page", back_populates="permissions")
