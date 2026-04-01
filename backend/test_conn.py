"""
Database connection test script.

This script tests the connection to the PostgreSQL database and performs basic checks
such as verifying the current database, server time, and user count.

Usage:
    python test_conn.py

It uses the default DATABASE_URL; update if needed for your environment.
"""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import os

# Database connection URL - update for your environment
DATABASE_URL = "postgresql+asyncpg://postgres:inter2018@localhost:5432/mini_erp"

async def test_connection():
    """
    Test database connection and perform basic health checks.

    Connects to PostgreSQL, retrieves database info, and checks user table.
    """
    print("🚀 Iniciando teste de conexão com o PostgreSQL...")
    engine = create_async_engine(DATABASE_URL)
    
    try:
        async with engine.connect() as conn:
            # Execute a simple query to test connection
            result = await conn.execute(text("SELECT current_database(), now();"))
            row = result.fetchone()
            print("✅ Conexão estabelecida com sucesso!")
            print(f"📂 Banco atual: {row[0]}")
            print(f"🕒 Hora no servidor: {row[1]}")
            
            # Check if users table exists and count records
            table_check = await conn.execute(text("SELECT count(*) FROM users;"))
            count = table_check.scalar()
            print(f"👥 Total de usuários cadastrados: {count}")
            
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_connection())