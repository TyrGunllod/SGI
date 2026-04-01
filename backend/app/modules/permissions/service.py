"""
Permission service for access control logic.

This module provides the PermissionService class that checks user permissions
for applications and pages, enabling fine-grained access control.

Operations:
    - Check if user has access to an application or specific page
"""

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Permission

class PermissionService:
    """
    Service for permission-related business logic.

    Handles access control checks based on user permissions.
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize the service with a database session.

        Args:
            db (AsyncSession): The async database session.
        """
        self.db = db

    async def has_access(self, user_id: str, app_slug: str, page_path: str = None) -> bool:
        """
        Check if a user has access to an application or specific page.

        Note: Admin users would have full access (bypass), but this is not implemented here.
        Currently checks for view permission on the app/page.

        Args:
            user_id (str): The ID of the user.
            app_slug (str): The slug of the application.
            page_path (str, optional): The path of the specific page.

        Returns:
            bool: True if the user has view access, False otherwise.
        """
        # Build query to find permission for user and app
        query = select(Permission).join(Permission.application).filter(
            Permission.user_id == user_id,
            Permission.application.slug == app_slug
        )
        
        # If page path specified, join and filter by page
        if page_path:
            query = query.join(Permission.page).filter(Permission.page.path == page_path)
            
        # Execute query
        result = await self.db.execute(query)
        permission = result.scalars().first()
        
        # Return view permission if found, else False
        return permission.can_view if permission else False