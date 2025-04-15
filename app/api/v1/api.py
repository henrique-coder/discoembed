# Third-party modules
from fastapi import APIRouter

# Local modules
from app.api.v1.endpoints import embed, health


api_router = APIRouter()
api_router.include_router(health.router, prefix="", tags=["Health"])
api_router.include_router(embed.router, prefix="", tags=["Embed"])
