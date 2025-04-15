# Third-party modules
from fastapi import APIRouter, status
from pydantic import BaseModel


router = APIRouter()


class HealthStatus(BaseModel):
    status: str = "ok"


@router.get(
    "/status",
    response_model=HealthStatus,
    status_code=status.HTTP_200_OK,
    tags=["Health"],
    summary="Perform a Health Check",
    response_description="Returns the health status of the API.",
)
async def health_check() -> HealthStatus:
    """Simple health check endpoint. Returns 'ok' status."""

    return HealthStatus(status="ok")
