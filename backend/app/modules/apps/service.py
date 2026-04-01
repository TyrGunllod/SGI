from .repository import AppRepository

class AppService:
    def __init__(self, repository: AppRepository):
        self.repository = repository

    async def list_apps(self):
        return await self.repository.get_all()

    async def create_app(self, app_data):
        # Aqui você poderia validar se o 'path' já existe, etc.
        return await self.repository.create(app_data)