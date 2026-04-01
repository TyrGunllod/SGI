import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import os

# Pega a URL do .env ou usa o padrão
DATABASE_URL = "postgresql+asyncpg://postgres:inter2018@localhost:5432/mini_erp"

async def test_connection():
    print("🚀 Iniciando teste de conexão com o PostgreSQL...")
    engine = create_async_engine(DATABASE_URL)
    
    try:
        async with engine.connect() as conn:
            # Tenta executar uma query simples
            result = await conn.execute(text("SELECT current_database(), now();"))
            row = result.fetchone()
            print(f"✅ Conexão estabelecida com sucesso!")
            print(f"📂 Banco atual: {row[0]}")
            print(f"🕒 Hora no servidor: {row[1]}")
            
            # Verifica se a tabela de usuários existe
            table_check = await conn.execute(text("SELECT count(*) FROM users;"))
            count = table_check.scalar()
            print(f"👥 Total de usuários cadastrados: {count}")
            
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_connection())