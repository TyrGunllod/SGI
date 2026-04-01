from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class LoginRequest(BaseModel):
    username: str
    password: str

class UserSummary(BaseModel):
    username: str
    is_admin: bool

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserSummary