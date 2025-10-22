"""
Cache manager for handling file downloads and local caching.

This module provides a robust cache management system with concurrent
access protection and atomic file operations.
"""

import fcntl
import tempfile
import time
import urllib.request
from pathlib import Path


class CacheManager:
    """
    Manages local file caching with concurrent access protection.

    This class handles downloading files from URLs and caching them locally,
    with built-in protection against concurrent access issues.
    """

    def __init__(self, cache_dir: Path, timeout: int = 30):
        """
        Initialize CacheManager.

        Args:
            cache_dir (Path): Directory for cached files
            timeout (int, optional): Timeout for downloads in seconds. Defaults to 30.
        """
        self.cache_dir = cache_dir
        self.timeout = timeout
        self.max_wait_time = 300  # 5 minutes max wait for concurrent downloads

    def ensure_file_cached(self, url: str, cache_file_path: Path) -> None:
        """
        Ensure the file is cached locally, downloading if necessary.
        Uses file locking to prevent concurrent access issues.

        Args:
            url (str): URL to download from
            cache_file_path (Path): Path where the cached file should be stored

        Raises:
            TimeoutError: If timeout occurs during download or waiting
            OSError: If file operations fail
        """
        if cache_file_path.exists():
            return

        # Create cache directory if it doesn't exist
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Use a lock file to prevent concurrent downloads
        lock_file_path = cache_file_path.with_suffix(".lock")

        try:
            with open(lock_file_path, "w") as lock_file:
                # Try to acquire exclusive lock
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)

                # Double-check if file was created by another process while waiting
                if cache_file_path.exists():
                    return

                print(f"Downloading data from: {url}")
                self._download_file(url, cache_file_path)
                print(f"Cached data to: {cache_file_path}")

        except (OSError, IOError) as e:
            if e.errno == 11:  # EAGAIN - lock would block
                self._wait_for_concurrent_download(cache_file_path)
            else:
                raise
        finally:
            # Clean up lock file
            self._cleanup_lock_file(lock_file_path)

    def _download_file(self, url: str, cache_file_path: Path) -> None:
        """
        Download file from URL to cache path using atomic operations.

        Args:
            url (str): URL to download from
            cache_file_path (Path): Path where the cached file should be stored

        Raises:
            urllib.error.URLError: If download fails
        """
        # Download to temporary file first for atomic operation
        with tempfile.NamedTemporaryFile(
            mode="wb", delete=False, dir=self.cache_dir, suffix=".tmp"
        ) as temp_file:
            # URL is already validated by PandasSource
            response = urllib.request.urlopen(url, timeout=self.timeout)  # nosec: B310
            temp_file.write(response.read())
            temp_file_path = Path(temp_file.name)

        # Atomically move temp file to final location
        temp_file_path.rename(cache_file_path)

    def _wait_for_concurrent_download(self, cache_file_path: Path) -> None:
        """
        Wait for another process to finish downloading the file.

        Args:
            cache_file_path (Path): Path to the file being downloaded

        Raises:
            TimeoutError: If waiting exceeds max_wait_time
        """
        print("Another process is downloading the file, waiting...")
        waited = 0
        while not cache_file_path.exists() and waited < self.max_wait_time:
            time.sleep(1)
            waited += 1

        if not cache_file_path.exists():
            raise TimeoutError(
                f"Timeout waiting for file download after {self.max_wait_time} seconds"
            )

    def _cleanup_lock_file(self, lock_file_path: Path) -> None:
        """
        Clean up the lock file safely.

        Args:
            lock_file_path (Path): Path to the lock file
        """
        try:
            lock_file_path.unlink(missing_ok=True)
        except Exception:  # nosec: B110 - cleanup errors should not stop execution
            pass

    def remove_cached_file(self, cache_file_path: Path) -> bool:
        """
        Remove a cached file.

        Args:
            cache_file_path (Path): Path to the cached file to remove

        Returns:
            bool: True if file was removed, False otherwise
        """
        try:
            if cache_file_path.exists():
                cache_file_path.unlink()
                return True
            return False
        except Exception:
            return False

    def clear_cache(self) -> int:
        """
        Clear all cached files in the cache directory.

        Returns:
            int: Number of files removed
        """
        removed_count = 0
        try:
            for file_path in self.cache_dir.glob("cached_*.csv"):
                if self.remove_cached_file(file_path):
                    removed_count += 1
        except Exception:  # nosec: B110 - cleanup errors should not stop execution
            pass
        return removed_count
