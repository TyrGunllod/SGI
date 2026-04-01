import asyncio
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.modules.users.controller import router as user_router
from app.modules.auth.controller import router as auth_router
from app.modules.apps.controller import router as apps_router

# Se for Windows, ajusta a política do loop de eventos
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


app = FastAPI(title="SGI-Sistema de Gestão Integrado API", version="1.0.0")

# Configuração de CORS para permitir que o Next.js (Porta 3000) acesse a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro das Rotas Modulares
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(user_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(apps_router, prefix="/api/v1/apps", tags=["Apps"])

@app.get("/health")
async def health_check():
    return {"status": "online", "message": "Backend operando normalmente"}