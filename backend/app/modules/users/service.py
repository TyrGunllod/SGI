from .repository import UserRepository
from .schemas import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, user_data: UserCreate):
        # Regra: Não permitir usernames duplicados
        existing = await self.repository.get_by_username(user_data.username)
        if existing:
            raise Exception("Username already exists")
            
        hashed_pwd = pwd_context.hash(user_data.password)
        # Lógica de mapeamento schema -> model
        return await self.repository.create(...)