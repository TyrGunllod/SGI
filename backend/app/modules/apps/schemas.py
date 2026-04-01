from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional

class AppBase(BaseModel):
    name: str
    description: Optional[str] = None
    icon: str = "Package"
    path: str
    is_active: bool = True

class AppCreate(AppBase):
    pass

class AppResponse(AppBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)