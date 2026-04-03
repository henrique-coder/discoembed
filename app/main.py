from __future__ import annotations

from contextlib import asynccontextmanager
from time import time
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, Awaitable, Callable

    from starlette.responses import Response

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from uvicorn import run

from app.api.v1.router import api_router
from app.core import settings
from app.services.validation import http_client


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[None, None]:

    logger.info(f"{settings.app_name} starting up — {settings.base_url}")
    yield
    logger.info(f"{settings.app_name} shutting down")
    await http_client.close()


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:

        response = await call_next(request)
        response.headers["Content-Security-Policy"] = (
            f"default-src {settings.csp_default_src}; "
            f"style-src {settings.csp_style_src}; "
            f"script-src {settings.csp_script_src};"
        )
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        response.headers["X-DNS-Prefetch-Control"] = "off"
        return response


class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:

        start_time = time()
        response = await call_next(request)
        process_time = time() - start_time
        response.headers["X-Process-Time"] = f"{process_time:.4f}"
        logger.debug(f"{request.method} {request.url.path} completed in {process_time:.4f}s")
        return response


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    version="1.0.0",
    description="A dynamic service that generates smart Discord video embeds without limitations for almost any video.",
    lifespan=lifespan,
)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(TimingMiddleware)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:

    logger.error(f"Validation error on {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )


app.include_router(api_router, prefix="/v1")


@app.get("/", include_in_schema=False)
async def root_redirect() -> RedirectResponse:

    return RedirectResponse(url="/v1/status", status_code=status.HTTP_302_FOUND)


if __name__ == "__main__":
    run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        log_level="debug" if settings.debug else "info",
        reload=settings.debug,
        proxy_headers=True,
        forwarded_allow_ips="*",
    )
