# Built-in modules
from typing import Optional

# Third-party modules
from flask import request as flask_request
from httpx import head, HTTPError
from validators import url as is_url, ValidationError


class CacheTools:
    """
    A class for cache tools.
    """

    @staticmethod
    def gen_cache_key(*args, **kwargs) -> str:
        """
        Generate a cache key for the current request.
        :param args: The arguments for the current request.
        :param kwargs: The keyword arguments for the current request.
        :return: A cache key for the current request.
        """

        return flask_request.url


def is_valid_url(url: str, online_check: bool = False) -> Optional[bool]:
    """
    Check if a URL is valid and reachable online.
    :param url: The URL to check.
    :param online_check: If True, check if the URL is reachable online.
    :return: True if the URL is valid, False if the URL is invalid, and None if the URL is unreachable online.
    """

    try:
        bool_value = bool(is_url(url))

        if not bool_value:
            return False
    except ValidationError:
        return False

    if online_check:
        try:
            response = head(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}, follow_redirects=True, timeout=15)
            return True if response.is_success or response.is_redirect else None
        except HTTPError:
            return None

    return bool_value
