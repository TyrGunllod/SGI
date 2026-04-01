from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class PermissionBase(BaseModel):
    user_id: UUID
    app_id: UUID
    page_id: Optional[UUID] = None
    can_view: bool = True
    can_edit: bool = False
    can_delete: bool = False

    class Config:
        from_attributes = True