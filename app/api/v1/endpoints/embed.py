# Third-party modules
from fastapi import APIRouter, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Local modules
from app.core.config import (
    DEFAULT_COVER_URL,
    DEFAULT_HEIGHT,
    DEFAULT_VIDEO_URL,
    DEFAULT_WIDTH,
    DISCORD_BOT_USER_AGENT,
    INVALID_COVER_URL,
    INVALID_URL_COVER_URL,
    INVALID_URL_VIDEO_URL,
    MISSING_COVER_URL,
    TEMPLATE_DIR,
)
from app.core.logging_config import logger
from app.services.validation import is_valid_url


router = APIRouter()
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


@router.get(
    "/",
    response_class=HTMLResponse,
    tags=["Embed"],
    summary="Generate Discord video embed HTML",
    response_description="HTML page with meta tags for Discord video embedding.",
)
async def get_embed(
    request: Request,
    url: str | None = Query(None, description="URL of the video to embed."),
    cover: str | None = Query(None, description="URL of the cover image."),
    width: str | None = Query(None, description="Width of the video player."),
    height: str | None = Query(None, description="Height of the video player."),
) -> HTMLResponse:
    user_agent = request.headers.get("user-agent", "")

    if user_agent != DISCORD_BOT_USER_AGENT:
        remote_addr = request.client.host if request.client else "unknown"
        logger.warning(f"Unauthorized access attempt from IP {remote_addr} with User-Agent: {user_agent}")
        logger.info("Returning default embed due to non-Discord User-Agent.")

        return templates.TemplateResponse(
            "embed.html", {"request": request, "url": DEFAULT_VIDEO_URL, "cover": DEFAULT_COVER_URL, "width": 1280, "height": 720}
        )

    logger.info(f"DiscordBot request received from IP: {request.client.host if request.client else 'unknown'}")

    final_url = url
    final_cover = cover
    final_width = width
    final_height = height

    if not final_url:
        logger.warning("No 'url' parameter provided. Using default video.")
        final_url = DEFAULT_VIDEO_URL
        final_cover = DEFAULT_COVER_URL
        final_width, final_height = 1280, 720
    else:
        is_valid = await is_valid_url(final_url, online_check=False)

        if not is_valid:
            logger.warning(f"Invalid 'url' format: {final_url}. Using error video.")
            final_url = INVALID_URL_VIDEO_URL
            final_cover = INVALID_URL_COVER_URL
            final_width, final_height = 1280, 720

    if final_url != INVALID_URL_VIDEO_URL:
        if not final_cover:
            logger.info(f"No 'cover' parameter provided for url '{final_url}'. Using default cover.")
            final_cover = MISSING_COVER_URL
        else:
            is_cover_valid = await is_valid_url(final_cover, online_check=True)
            if is_cover_valid is None:
                logger.warning(f"Cover URL '{final_cover}' unreachable. Using error cover.")
                final_cover = INVALID_COVER_URL
            elif is_cover_valid is False:
                logger.warning(f"Invalid 'cover' format: {final_cover}. Using error cover.")
                final_cover = INVALID_COVER_URL

    if final_width is None or final_height is None or final_width <= 0 or final_height <= 0:
        if width is not None or height is not None:
            logger.warning(f"Invalid width/height provided: w={width}, h={height}. Using defaults.")

        final_width = DEFAULT_WIDTH
        final_height = DEFAULT_HEIGHT

    logger.info(f"Rendering embed for URL: {final_url}, Cover: {final_cover}, Size: {final_width}x{final_height}")

    return templates.TemplateResponse(
        "embed.html", {"request": request, "url": final_url, "cover": final_cover, "width": final_width, "height": final_height}
    )
