from __future__ import annotations

from curl_cffi.requests import AsyncSession
from loguru import logger
from pydantic import HttpUrl, ValidationError


class _HttpClient:
    def __init__(self) -> None:
        self._session: AsyncSession | None = None

    def _get_session(self) -> AsyncSession:
        if self._session is None:
            self._session = AsyncSession(
                impersonate="chrome",
                allow_redirects=True,
                timeout=15,
                verify=False,
            )
        return self._session

    async def head(self, url: str) -> int:
        session = self._get_session()
        response = await session.head(url)
        return response.status_code

    async def close(self) -> None:
        if self._session is not None:
            await self._session.close()
            self._session = None
            logger.info("HTTP client closed")


http_client = _HttpClient()


def is_valid_url_format(url: str) -> bool:
    try:
        HttpUrl(url)
    except ValidationError:
        logger.debug(f"Invalid URL format: {url}")
        return False
    else:
        return True


async def is_url_reachable(url: str) -> bool | None:
    if not is_valid_url_format(url):
        return False

    try:
        status_code = await http_client.head(url)
    except Exception as exc:
        logger.error(f"HTTP error checking URL {url}: {exc}")
        return None
    else:
        if 200 <= status_code < 400:
            logger.debug(f"URL reachable: {url} (status={status_code})")
            return True

        logger.warning(f"URL unreachable: {url} (status={status_code})")
        return None
