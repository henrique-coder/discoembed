from __future__ import annotations

from fastapi import APIRouter, status
from pydantic import BaseModel

from app.core import settings


router = APIRouter()


class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = settings.app_name
    base_url: str = settings.base_url


@router.get(
    "/status",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    response_description="Returns the health status of the API.",
)
async def health_check() -> HealthResponse:

    return HealthResponse()
