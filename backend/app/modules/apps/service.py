"""
Application service layer for business logic.

This module provides the AppService class that handles application management operations,
including listing and creating applications.

Operations:
    - List all active applications
    - Create new applications
"""

from .repository import AppRepository

class AppService:
    """
    Service for application-related business logic.

    Manages application operations with potential validation.
    """

    def __init__(self, repository: AppRepository):
        """
        Initialize the service with an app repository.

        Args:
            repository (AppRepository): The application data repository.
        """
        self.repository = repository

    async def list_apps(self):
        """
        Retrieve a list of all active applications.

        Returns:
            list[AppModel]: List of active applications.
        """
        return await self.repository.get_all()

    async def create_app(self, app_data):
        """
        Create a new application.

        Note: Additional validation (e.g., unique path) could be added here.

        Args:
            app_data: Dictionary of application data.

        Returns:
            AppModel: The created application instance.
        """
        # Potential validation for path uniqueness, etc.
        return await self.repository.create(app_data)