"""
Pydantic schemas for application data.

This module defines the data models for applications, used for validation,
creation, and response serialization in the apps API.

Schemas:
    - AppBase: Common application fields
    - AppCreate: For creating new applications
    - AppResponse: For API responses with ID
"""

from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional

class AppBase(BaseModel):
    """
    Base schema for application data.

    Contains common fields for application definitions.
    """
    name: str  # Application name
    slug: str  # Unique slug identifier
    description: Optional[str] = None  # Optional description
    icon: str = "Package"  # Icon name
    path: str  # URL path
    is_active: bool = True  # Active status

class AppCreate(AppBase):
    """
    Schema for creating new applications.

    Inherits all fields from AppBase.
    """
    pass

class AppResponse(AppBase):
    """
    Schema for application data in API responses.

    Includes the application ID.
    """
    id: UUID  # Application UUID
    model_config = ConfigDict(from_attributes=True)  # Enables SQLAlchemy conversion