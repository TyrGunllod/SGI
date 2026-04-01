"""
Pydantic schemas for permission data.

This module defines the data models for permissions, used for validation
and serialization in permission-related operations.

Schemas:
    - PermissionBase: Base schema for permission data
"""

from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class PermissionBase(BaseModel):
    """
    Base schema for permission data.

    Defines the structure for user permissions on applications and pages.
    """
    user_id: UUID  # ID of the user
    app_id: UUID   # ID of the application
    page_id: Optional[UUID] = None  # Optional ID of the specific page
    can_view: bool = True   # Permission to view
    can_edit: bool = False  # Permission to edit
    can_delete: bool = False  # Permission to delete

    class Config:
        from_attributes = True  # Enables conversion from SQLAlchemy models