"""
Main module for the SGI (Sistema de Gestão Integrado) API.

This module initializes the FastAPI application, configures CORS middleware for cross-origin requests,
sets up event loop policy for Windows compatibility, and includes modular routers for authentication,
users, and apps management. It also provides a health check endpoint.

Author: [Your Name or Team]
Version: 1.0.0
"""

import asyncio
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.modules.users.controller import router as user_router
from app.modules.auth.controller import router as auth_router
from app.modules.apps.controller import router as apps_router

# Adjust event loop policy for Windows compatibility to avoid issues with asyncio
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Initialize FastAPI application with title and version
app = FastAPI(title="SGI-Sistema de Gestão Integrado API", version="1.0.0")

# Configure CORS middleware to allow requests from the Next.js frontend on localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers for different modules with API versioning and tags
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(user_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(apps_router, prefix="/api/v1/apps", tags=["Apps"])

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify if the backend is operational.

    Returns:
        dict: A dictionary with status and message indicating the service is online.
    """
    return {"status": "online", "message": "Backend operando normalmente"}