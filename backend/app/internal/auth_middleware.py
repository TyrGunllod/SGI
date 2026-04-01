"""
Authentication middleware for app access control.

This module provides a dependency function to check if the current user has access
to a specific application based on permissions. It integrates with the permission service
to enforce access control in FastAPI routes.

Dependencies:
    - app.core.deps for user authentication
    - app.database for database sessions
    - app.modules.permissions.service for permission checks
"""

from fastapi import HTTPException, Depends, status
from app.core.deps import get_current_user
from app.database import get_db
from app.modules.permissions.service import PermissionService

def check_app_access(app_slug: str):
    """
    Create a dependency to check if the authenticated user has access to the specified app.

    This function returns a dependency that verifies user permissions for the given app slug.
    If access is denied, it raises a 403 Forbidden exception.

    Args:
        app_slug (str): The slug identifier of the application to check access for.

    Returns:
        callable: A FastAPI dependency function that returns the user ID if access is granted.

    Raises:
        HTTPException: 403 Forbidden if the user lacks permission for the app.
    """
    async def _check(user_id: str = Depends(get_current_user), db=Depends(get_db)):
        # Initialize permission service with database session
        service = PermissionService(db)
        # Check if user has access to the app
        if not await service.has_access(user_id, app_slug):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Você não tem permissão para acessar o app: {app_slug}"
            )
        # Return user ID if access is granted
        return user_id
    return _check