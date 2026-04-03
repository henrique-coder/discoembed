from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.endpoints import embed, health


api_router = APIRouter()
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(embed.router, tags=["Embed"])
