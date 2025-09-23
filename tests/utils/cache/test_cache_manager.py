"""
Tests for the CacheManager class in src.utils.cache.cache_manager module.
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch
from urllib.error import URLError

import pytest

from src.utils.cache.cache_manager import CacheManager


@pytest.fixture
def temp_cache_dir():
    """Create a temporary directory for cache testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def cache_manager(temp_cache_dir):
    """Create a CacheManager instance with temporary cache directory."""
    return CacheManager(temp_cache_dir, timeout=5)


class TestCacheManagerInitialization:
    """Test CacheManager initialization."""

    def test_init_with_defaults(self, temp_cache_dir):
        """Test initialization with default timeout."""
        manager = CacheManager(temp_cache_dir)
        assert manager.cache_dir == temp_cache_dir
        assert manager.timeout == 30
        assert manager.max_wait_time == 300

    def test_init_with_custom_timeout(self, temp_cache_dir):
        """Test initialization with custom timeout."""
        manager = CacheManager(temp_cache_dir, timeout=60)
        assert manager.cache_dir == temp_cache_dir
        assert manager.timeout == 60


class TestEnsureFileCached:
    """Test ensure_file_cached functionality."""

    def test_file_already_exists_does_nothing(self, cache_manager, temp_cache_dir):
        """Test that existing files are not re-downloaded."""
        # Create an existing file
        cache_file = temp_cache_dir / "test_file.csv"
        cache_file.write_text("existing content")

        # Mock urllib to ensure it's not called
        with patch(
            "src.utils.cache.cache_manager.urllib.request.urlopen"
        ) as mock_urlopen:
            cache_manager.ensure_file_cached("http://example.com/data.csv", cache_file)
            mock_urlopen.assert_not_called()

    @patch("src.utils.cache.cache_manager.urllib.request.urlopen")
    @patch("src.utils.cache.cache_manager.fcntl.flock")
    def test_successful_download(
        self, mock_flock, mock_urlopen, cache_manager, temp_cache_dir
    ):
        """Test successful file download and caching."""
        # Setup mocks
        mock_response = MagicMock()
        mock_response.read.return_value = b"test,data\n1,2\n3,4"
        mock_urlopen.return_value = mock_response

        cache_file = temp_cache_dir / "new_file.csv"
        test_url = "http://example.com/data.csv"

        # Execute
        cache_manager.ensure_file_cached(test_url, cache_file)

        # Verify
        assert cache_file.exists()
        assert cache_file.read_text() == "test,data\n1,2\n3,4"
        mock_urlopen.assert_called_once_with(test_url, timeout=5)

    @patch("src.utils.cache.cache_manager.urllib.request.urlopen")
    @patch("src.utils.cache.cache_manager.fcntl.flock")
    def test_download_creates_cache_directory(
        self, mock_flock, mock_urlopen, temp_cache_dir
    ):
        """Test that cache directory is created if it doesn't exist."""
        # Setup mocks
        mock_response = MagicMock()
        mock_response.read.return_value = b"test data"
        mock_urlopen.return_value = mock_response

        # Use non-existent subdirectory
        cache_subdir = temp_cache_dir / "subdir" / "cache"
        cache_manager = CacheManager(cache_subdir, timeout=5)
        cache_file = cache_subdir / "test.csv"

        # Execute
        cache_manager.ensure_file_cached("http://example.com/data.csv", cache_file)

        # Verify directory was created
        assert cache_subdir.exists()
        assert cache_file.exists()

    @patch("src.utils.cache.cache_manager.urllib.request.urlopen")
    @patch("src.utils.cache.cache_manager.fcntl.flock")
    def test_download_timeout_error(
        self, mock_flock, mock_urlopen, cache_manager, temp_cache_dir
    ):
        """Test handling of download timeout."""
        # Setup mock to raise timeout
        mock_urlopen.side_effect = URLError("timeout")

        cache_file = temp_cache_dir / "timeout_file.csv"

        # Execute and verify exception
        with pytest.raises(URLError):
            cache_manager.ensure_file_cached("http://example.com/data.csv", cache_file)

    @patch("src.utils.cache.cache_manager.urllib.request.urlopen")
    @patch("src.utils.cache.cache_manager.fcntl.flock")
    @patch("src.utils.cache.cache_manager.time.sleep")
    def test_concurrent_download_wait(
        self, mock_sleep, mock_flock, mock_urlopen, cache_manager, temp_cache_dir
    ):
        """Test waiting for concurrent download to complete."""
        # Setup flock to raise EAGAIN (resource temporarily unavailable)
        mock_flock.side_effect = [OSError(11, "Resource temporarily unavailable"), None]

        cache_file = temp_cache_dir / "concurrent_file.csv"

        # Create the file after some "waiting" to simulate another process completing
        def create_file_after_sleep(*args):
            cache_file.write_text("created by other process")

        mock_sleep.side_effect = create_file_after_sleep

        # Execute
        cache_manager.ensure_file_cached("http://example.com/data.csv", cache_file)

        # Verify file exists and sleep was called (waiting behavior)
        assert cache_file.exists()
        mock_sleep.assert_called()

    @patch("src.utils.cache.cache_manager.urllib.request.urlopen")
    @patch("src.utils.cache.cache_manager.fcntl.flock")
    @patch("src.utils.cache.cache_manager.time.sleep")
    def test_concurrent_download_timeout(
        self, mock_sleep, mock_flock, mock_urlopen, temp_cache_dir
    ):
        """Test timeout when waiting for concurrent download."""
        # Create manager with very short max_wait_time for testing
        cache_manager = CacheManager(temp_cache_dir, timeout=5)
        cache_manager.max_wait_time = 2  # 2 seconds max wait

        # Setup flock to always raise EAGAIN
        mock_flock.side_effect = OSError(11, "Resource temporarily unavailable")

        cache_file = temp_cache_dir / "timeout_concurrent.csv"

        # Execute and verify timeout
        with pytest.raises(TimeoutError, match="Timeout waiting for file download"):
            cache_manager.ensure_file_cached("http://example.com/data.csv", cache_file)

    @patch("src.utils.cache.cache_manager.urllib.request.urlopen")
    @patch("src.utils.cache.cache_manager.fcntl.flock")
    def test_double_check_file_exists_after_lock(
        self, mock_flock, mock_urlopen, cache_manager, temp_cache_dir
    ):
        """Test double-check scenario where file exists after
        getting lock but before download."""
        cache_file = temp_cache_dir / "double_check.csv"

        # Mock flock to succeed immediately (no concurrent access)
        mock_flock.return_value = None

        # Create the file after lock is acquired but before download
        # This simulates another process completing just after we get the lock
        def create_file_side_effect(*args, **kwargs):
            cache_file.write_text("created by other process during lock")
            return None

        mock_flock.side_effect = create_file_side_effect

        # Execute - should not call urlopen because file exists after double-check
        cache_manager.ensure_file_cached("http://example.com/data.csv", cache_file)

        # Verify file exists and urlopen was not called (no download happened)
        assert cache_file.exists()
        assert cache_file.read_text() == "created by other process during lock"
        mock_urlopen.assert_not_called()


class TestRemoveCachedFile:
    """Test remove_cached_file functionality."""

    def test_remove_existing_file(self, cache_manager, temp_cache_dir):
        """Test removing an existing cached file."""
        # Create a test file
        cache_file = temp_cache_dir / "test_remove.csv"
        cache_file.write_text("test content")

        # Remove file
        result = cache_manager.remove_cached_file(cache_file)

        # Verify
        assert result is True
        assert not cache_file.exists()

    def test_remove_nonexistent_file(self, cache_manager, temp_cache_dir):
        """Test removing a non-existent file."""
        cache_file = temp_cache_dir / "nonexistent.csv"

        result = cache_manager.remove_cached_file(cache_file)

        assert result is False

    def test_remove_file_permission_error(self, cache_manager, temp_cache_dir):
        """Test handling permission errors during file removal."""
        cache_file = temp_cache_dir / "permission_test.csv"
        cache_file.write_text("test content")

        # Mock unlink to raise permission error
        with patch.object(Path, "unlink", side_effect=PermissionError("Access denied")):
            result = cache_manager.remove_cached_file(cache_file)
            assert result is False


class TestClearCache:
    """Test clear_cache functionality."""

    def test_clear_cache_removes_cached_files(self, cache_manager, temp_cache_dir):
        """Test that clear_cache removes all cached files."""
        # Create several cached files
        (temp_cache_dir / "cached_file1.csv").write_text("data1")
        (temp_cache_dir / "cached_file2.csv").write_text("data2")
        (temp_cache_dir / "cached_file3.csv").write_text("data3")
        # Create non-cached file (should not be removed)
        (temp_cache_dir / "other_file.txt").write_text("other")

        # Clear cache
        removed_count = cache_manager.clear_cache()

        # Verify
        assert removed_count == 3
        assert not (temp_cache_dir / "cached_file1.csv").exists()
        assert not (temp_cache_dir / "cached_file2.csv").exists()
        assert not (temp_cache_dir / "cached_file3.csv").exists()
        assert (temp_cache_dir / "other_file.txt").exists()  # Should remain

    def test_clear_cache_empty_directory(self, cache_manager, temp_cache_dir):
        """Test clear_cache on empty directory."""
        removed_count = cache_manager.clear_cache()
        assert removed_count == 0

    def test_clear_cache_handles_errors(self, cache_manager, temp_cache_dir):
        """Test that clear_cache handles errors gracefully."""
        # Create a cached file
        (temp_cache_dir / "cached_error.csv").write_text("data")

        # Mock glob to raise an exception
        with patch.object(Path, "glob", side_effect=OSError("Access denied")):
            removed_count = cache_manager.clear_cache()
            assert removed_count == 0  # Should handle error gracefully


class TestPrivateMethods:
    """Test private helper methods."""

    def test_cleanup_lock_file_success(self, cache_manager, temp_cache_dir):
        """Test successful lock file cleanup."""
        lock_file = temp_cache_dir / "test.lock"
        lock_file.write_text("lock")

        cache_manager._cleanup_lock_file(lock_file)

        assert not lock_file.exists()

    def test_cleanup_lock_file_nonexistent(self, cache_manager, temp_cache_dir):
        """Test cleanup of non-existent lock file."""
        lock_file = temp_cache_dir / "nonexistent.lock"

        # Should not raise exception
        cache_manager._cleanup_lock_file(lock_file)

    def test_cleanup_lock_file_handles_errors(self, cache_manager, temp_cache_dir):
        """Test that cleanup handles errors gracefully."""
        lock_file = temp_cache_dir / "error.lock"
        lock_file.write_text("lock")

        # Mock unlink to raise exception
        with patch.object(Path, "unlink", side_effect=OSError("Permission denied")):
            # Should not raise exception
            cache_manager._cleanup_lock_file(lock_file)
