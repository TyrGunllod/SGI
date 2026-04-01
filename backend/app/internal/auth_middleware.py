from fastapi import HTTPException, Depends, status
from app.core.deps import get_current_user
from app.database import get_db
from app.modules.permissions.service import PermissionService

def check_app_access(app_slug: str):
    async def _check(user_id: str = Depends(get_current_user), db=Depends(get_db)):
        service = PermissionService(db)
        if not await service.has_access(user_id, app_slug):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Você não tem permissão para acessar o app: {app_slug}"
            )
        return user_id
    return _check