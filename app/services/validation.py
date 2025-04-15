# Third-party modules
from httpx import AsyncClient, RequestError
from validators import ValidationError
from validators import url as is_url_valid_format

# Local modules
from app.core.logging_config import logger


# Use a shared async client for performance
async_client = AsyncClient(
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    },
    follow_redirects=True,
    timeout=15,
)


async def is_valid_url(url_to_check: str, online_check: bool = False) -> bool | None:
    """
    Asynchronously check if a URL is valid and optionally reachable online.

    Params:
        url_to_check: The URL to check.
        online_check: If True, check if the URL is reachable online. Defaults to False.

    Returns:
        True if valid (and reachable if checked), False if invalid format, None if unreachable online.
    """

    try:
        if not is_url_valid_format(url_to_check):
            logger.debug(f"URL format invalid: {url_to_check}")
            return False
    except ValidationError:
        logger.debug(f"URL validation error for: {url_to_check}")
        return False

    if online_check:
        try:
            response = await async_client.head(url_to_check)

            if response.is_success or response.is_redirect:
                logger.debug(f"URL online check successful: {url_to_check} (Status: {response.status_code})")
                return True
            else:
                logger.warning(f"URL online check failed: {url_to_check} (Status: {response.status_code})")
                return None
        except RequestError as e:
            logger.error(f"HTTP request error checking URL {url_to_check}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error checking URL {url_to_check}: {e}")
            return None

    logger.debug(f"URL format valid (online check skipped): {url_to_check}")
    return True


async def close_httpx_client() -> None:
    """Closes the shared httpx client."""

    await async_client.aclose()
    logger.info("HTTPX AsyncClient closed.")
