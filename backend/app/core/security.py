"""
Security utilities module for password hashing and JWT token management.

This module provides functions for creating and verifying access tokens using JWT,
as well as hashing and verifying passwords using bcrypt. It uses environment variables
for configuration to keep secrets secure.

Environment Variables:
    SECRET_KEY: Secret key for JWT signing (default: development key)
    ACCESS_TOKEN_EXPIRE_MINUTES: Token expiration time in minutes (default: 30)

Dependencies:
    - jose for JWT encoding/decoding
    - passlib for password hashing
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
import os

# Security configuration from environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-2026")
ALGORITHM = "HS256"  # HMAC SHA-256 for JWT signing
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Default token expiration time

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(subject: Union[str, Any]) -> str:
    """
    Create a JWT access token for the given subject (user ID).

    The token includes expiration time, subject, and token type claims.

    Args:
        subject (Union[str, Any]): The user ID or identifier to encode in the token.

    Returns:
        str: The encoded JWT access token.
    """
    # Calculate expiration time
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Payload to encode
    to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
    # Encode and return the token
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against its hashed version.

    Args:
        plain_password (str): The plain text password.
        hashed_password (str): The hashed password from the database.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash a plain password using bcrypt.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)