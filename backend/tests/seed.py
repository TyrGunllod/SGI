import asyncio
import uuid

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from app.modules.users.models import User
from app.core.security import get_password_hash


DATABASE_URL = "postgresql+asyncpg://postgres:inter2018@localhost:5432/mini_erp"


async def create_first_user():

    engine = create_async_engine(DATABASE_URL, echo=True)

    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session:

        username = "admin"
        password = "admin123"

        # 🔎 verifica se já existe
        result = await session.execute(
            select(User).where(User.username == username)
        )

        user = result.scalar_one_or_none()

        if user:
            print("⚠️ Usuário admin já existe")
            return

        hashed_password = get_password_hash(password)

        new_user = User(
            id=uuid.uuid4(),
            username=username,
            hashed_password=hashed_password,
            full_name="Administrador do Sistema",
            is_active=True,
            is_admin=True
        )

        session.add(new_user)

        await session.commit()

        print("✅ Usuário criado com sucesso")
        print("👤 username:", username)
        print("🔑 password:", password)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(create_first_user())