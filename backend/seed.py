"""
Database seeding script for initial data.

This script creates the first admin user in the system if it doesn't already exist.
It should be run after database setup to bootstrap the application with an admin account.

Default credentials:
    Username: superuser
    Password: 1234567890

Usage:
    python seed.py

Note: Change the default password in production.
"""

import asyncio
import uuid

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from app.modules.users.models import User
from app.core.security import get_password_hash

# Database connection URL - update for your environment
DATABASE_URL = "postgresql+asyncpg://postgres:inter2018@localhost:5432/mini_erp"

async def create_first_user():
    """
    Create the first admin user if it doesn't exist.

    Sets up a superuser account with admin privileges for initial system access.
    """
    # Create async engine with logging enabled
    engine = create_async_engine(DATABASE_URL, echo=True)

    # Configure async session maker
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session:
        # Default admin credentials
        username = "superuser"
        password = "1234567890"

        # Check if admin user already exists
        result = await session.execute(
            select(User).where(User.username == username)
        )

        user = result.scalar_one_or_none()

        if user:
            print("⚠️ Usuário admin já existe")
            return

        # Hash the password
        hashed_password = get_password_hash(password)

        # Create new admin user
        new_user = User(
            id=uuid.uuid4(),
            username=username,
            hashed_password=hashed_password,
            full_name="Administrador do Sistema",
            is_active=True,
            is_admin=True
        )

        # Add and commit to database
        session.add(new_user)
        await session.commit()

        print("✅ Usuário criado com sucesso")
        print("👤 username:", username)
        print("🔑 password:", password)

    # Dispose of the engine
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(create_first_user())