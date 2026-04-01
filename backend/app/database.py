"""
Database configuration module for the SGI API.

This module sets up the asynchronous SQLAlchemy engine for PostgreSQL,
configures session management, and defines a base class with automatic
timestamps for all database models. It also provides a dependency function
for obtaining database sessions in FastAPI routes.

Environment Variables:
    DATABASE_URL: PostgreSQL connection string (default: local development setup)

Dependencies:
    - SQLAlchemy for ORM and async database operations
    - asyncpg for PostgreSQL async driver
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, DateTime, func
import os

# Database connection URL from environment variable, with default for local development
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:inter2018@127.0.0.1:5432/mini_erp")

# Create asynchronous engine with connection pooling and health checks
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging in development
    pool_pre_ping=True,      # Verify connection health before use
    pool_recycle=1800,       # Recycle connections every 30 minutes to prevent stale connections
    pool_size=10,            # Maximum number of persistent connections
    max_overflow=20          # Additional connections allowed during peak load
)

# Configure async session maker for database transactions
SessionLocal = async_sessionmaker(
    autocommit=False,  # Transactions must be committed explicitly
    autoflush=False,   # Changes are not flushed automatically
    bind=engine,       # Bind to the async engine
    class_=AsyncSession,  # Use AsyncSession for async operations
    expire_on_commit=False  # Keep objects loaded after commit
)

class Base(DeclarativeBase):
    """
    Base class for all database models.

    Provides automatic timestamp columns for creation and update times.
    All models should inherit from this class.
    """
    # Automatic timestamp for record creation
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # Automatic timestamp for record updates
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

async def get_db():
    """
    Dependency function to provide database sessions to FastAPI routes.

    Yields an AsyncSession instance for database operations.
    Automatically closes the session after use.
    """
    async with SessionLocal() as session:
        yield session