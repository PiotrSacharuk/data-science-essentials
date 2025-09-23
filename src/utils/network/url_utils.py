"""
URL utilities for validating and processing URLs.

This module provides utility functions for working with URLs,
including validation and cache path generation.
"""

import hashlib
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse


def is_url(path: str) -> bool:
    """
    Check if the given path is a valid URL.

    Args:
        path (str): Path to check

    Returns:
        bool: True if path is a URL, False otherwise
    """
    try:
        result = urlparse(path)
        return all([result.scheme, result.netloc]) and result.scheme in [
            "http",
            "https",
        ]
    except Exception:
        return False


def generate_cache_filename(url: str, extension: str = ".csv") -> str:
    """
    Generate a cache filename for the given URL.

    Args:
        url (str): URL to generate cache filename for
        extension (str, optional): File extension. Defaults to ".csv".

    Returns:
        str: Generated cache filename
    """
    url_hash = hashlib.md5(url.encode()).hexdigest()
    return f"cached_{url_hash}{extension}"


def get_cached_file_path(url: str, cache_dir: Path, extension: str = ".csv") -> Path:
    """
    Generate a cached file path for the given URL.

    Args:
        url (str): URL to generate cache path for
        cache_dir (Path): Directory for cached files
        extension (str, optional): File extension. Defaults to ".csv".

    Returns:
        Path: Path to the cached file
    """
    filename = generate_cache_filename(url, extension)
    return cache_dir / filename


def validate_url(url: str, allowed_schemes: Optional[list] = None) -> bool:
    """
    Validate URL with additional security checks.

    Args:
        url (str): URL to validate
        allowed_schemes (list, optional): List of allowed schemes.
                                          Defaults to ['http', 'https'].

    Returns:
        bool: True if URL is valid and allowed, False otherwise
    """
    if allowed_schemes is None:
        allowed_schemes = ["http", "https"]

    try:
        result = urlparse(url)

        # Check basic URL structure
        if not all([result.scheme, result.netloc]):
            return False

        # Check allowed schemes
        if result.scheme not in allowed_schemes:
            return False

        # Basic security checks
        if result.netloc.lower() in ["localhost", "127.0.0.1", "0.0.0.0"]:
            return False

        return True
    except Exception:
        return False
