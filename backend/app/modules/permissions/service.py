from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Permission

class PermissionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def has_access(self, user_id: str, app_slug: str, page_path: str = None) -> bool:
        # Se for admin, acesso total (bypass)
        # (Aqui buscaríamos o campo is_admin do user no banco)
        
        query = select(Permission).join(Permission.application).filter(
            Permission.user_id == user_id,
            Permission.application.slug == app_slug
        )
        
        if page_path:
            query = query.join(Permission.page).filter(Permission.page.path == page_path)
            
        result = await self.db.execute(query)
        permission = result.scalars().first()
        
        return permission.can_view if permission else False