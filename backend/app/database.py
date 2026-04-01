from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, DateTime, func
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:inter2018@127.0.0.1:5432/mini_erp")

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,      # Verifica se a conexão caiu antes de usar
    pool_recycle=1800,       # Recicla conexões a cada 30 min
    pool_size=10,            # Limite de conexões simultâneas
    max_overflow=20          # Conexões extras permitidas em pico
)
SessionLocal = async_sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine, 
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    # Mixin para timestamps automáticos em todas as tabelas
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),onupdate=func.now())

async def get_db():
    async with SessionLocal() as session:
        yield session