# Standard modules
from collections.abc import Callable
from time import time

# Third-party modules
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from uvicorn import run

# Local modules
from app.api.v1.api import api_router
from app.core.config import ALLOWED_ORIGINS, APP_NAME, CSP_DEFAULT_SRC, CSP_SCRIPT_SRC, CSP_STYLE_SRC, DEBUG, HOST, PORT
from app.core.logging_config import logger, setup_logging
from app.services.validation import close_httpx_client


# Setup logging first
setup_logging()


# --- Security Headers Middleware ---
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> JSONResponse:
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = (
            f"default-src {CSP_DEFAULT_SRC}; style-src {CSP_STYLE_SRC}; script-src {CSP_SCRIPT_SRC};"
        )
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        return response


# --- Timing Middleware ---
class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> JSONResponse:
        start_time = time()
        response = await call_next(request)
        process_time = time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        logger.debug(f"Request {request.method} {request.url.path} processed in {process_time:.4f} seconds")

        return response


# --- App Initialization ---
app = FastAPI(
    title=APP_NAME,
    debug=DEBUG,
    version="0.0.1",
    description="A dynamic website that is capable of generating smart Discord embeds without any limitations for almost any video.",
)

# --- Middleware Setup ---

# Security Headers
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    CORSMiddleware, allow_origins=ALLOWED_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(TimingMiddleware)

# GZip Compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Timing
app.add_middleware(TimingMiddleware)


# --- Exception Handlers ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    logger.error(f"Validation error for request {request.url.path}: {exc.errors()}")
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": exc.errors(), "body": exc.body})


# --- Routers ---
app.include_router(api_router, prefix="/v1")


# --- Root Redirect ---
@app.get("/", include_in_schema=False)
async def root_redirect() -> RedirectResponse:
    return RedirectResponse(url="/v1/status", status_code=status.HTTP_302_FOUND)


# --- Startup and Shutdown Events ---
@app.on_event("startup")
async def startup_event() -> None:
    """Tasks to run when the application starts."""

    logger.info("Application startup...")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Tasks to run when the application shuts down."""

    logger.info("Application shutdown...")
    await close_httpx_client()


# --- Main entry point for Uvicorn ---
if __name__ == "__main__":
    run(
        "app.main:app",
        host=HOST,
        port=PORT,
        log_level="info" if not DEBUG else "debug",
        reload=DEBUG,
        proxy_headers=True,
        forwarded_allow_ips="*",
    )
