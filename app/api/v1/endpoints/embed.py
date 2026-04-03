from __future__ import annotations

from fastapi import APIRouter, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from loguru import logger

from app.core import settings
from app.services.validation import is_url_reachable, is_valid_url_format


router = APIRouter()
templates = Jinja2Templates(directory=str(settings.template_dir))


def _render_embed(
    request: Request,
    url: str,
    cover: str,
    width: int,
    height: int,
) -> HTMLResponse:

    context = {
        "url": url,
        "cover": cover,
        "width": width,
        "height": height,
        "APP_NAME": settings.app_name,
    }
    return templates.TemplateResponse(request, "embed.html", context)


@router.get(
    "/",
    response_class=HTMLResponse,
    summary="Generate Discord Video Embed",
    response_description="HTML page with Open Graph and Twitter Card meta tags for Discord video embedding.",
)
async def get_embed(
    request: Request,
    url: str | None = Query(None, description="Direct URL of the video to embed."),
    cover: str | None = Query(None, description="Direct URL of the cover/thumbnail image."),
    width: int = Query(settings.default_width, gt=0, description="Width of the video player in pixels."),
    height: int = Query(
        settings.default_height,
        gt=0,
        description="Height of the video player in pixels.",
    ),
) -> HTMLResponse:

    user_agent = request.headers.get("user-agent", "")

    if user_agent != settings.discord_bot_user_agent:
        remote_addr = request.client.host if request.client else "unknown"
        logger.info(f"Non-Discord request from {remote_addr} (UA: {user_agent[:80]})")
        return _render_embed(request, settings.default_video_url, settings.default_cover_url, 1280, 720)

    logger.info(f"Discord bot request from {request.client.host if request.client else 'unknown'}")

    if not url:
        logger.warning("Missing 'url' parameter, using default video")
        return _render_embed(request, settings.default_video_url, settings.default_cover_url, 1280, 720)

    if not is_valid_url_format(url):
        logger.warning(f"Invalid URL format: {url}")
        return _render_embed(
            request,
            settings.invalid_url_video_url,
            settings.invalid_url_cover_url,
            1280,
            720,
        )

    final_cover = cover
    if not final_cover:
        logger.info(f"No cover provided for {url}, using missing cover placeholder")
        final_cover = settings.missing_cover_url
    else:
        cover_status = await is_url_reachable(final_cover)
        if cover_status is None:
            logger.warning(f"Cover URL unreachable: {final_cover}")
            final_cover = settings.invalid_cover_url
        elif not cover_status:
            logger.warning(f"Invalid cover URL format: {final_cover}")
            final_cover = settings.invalid_cover_url

    logger.info(f"Rendering embed: url={url}, cover={final_cover}, size={width}x{height}")
    return _render_embed(request, url, final_cover, width, height)
