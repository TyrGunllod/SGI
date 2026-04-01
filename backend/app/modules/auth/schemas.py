"""
Pydantic schemas for authentication requests and responses.

This module defines the data models used for login, token responses,
user summaries, and refresh token requests in the authentication API.

Schemas:
    - LoginRequest: Credentials for user login
    - UserSummary: Basic user information in responses
    - TokenResponse: JWT tokens and user data after login
    - RefreshTokenRequest: Request to refresh access token
"""

from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class LoginRequest(BaseModel):
    """
    Schema for user login request.

    Contains the username and password for authentication.
    """
    username: str
    password: str

class UserSummary(BaseModel):
    """
    Schema for basic user information in API responses.

    Includes username and admin status.
    """
    username: str
    is_admin: bool

class TokenResponse(BaseModel):
    """
    Schema for authentication token response.

    Contains access and refresh tokens, token type, and user summary.
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserSummary

class RefreshTokenRequest(BaseModel):
    """
    Schema for refresh token request.

    Used to obtain new access tokens using a valid refresh token.
    """
    refresh_token: str