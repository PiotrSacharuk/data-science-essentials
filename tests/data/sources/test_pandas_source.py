"""
Tests for the PandasSource class in src.data.sources.pandas_source module.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.data.sources.pandas_source import PandasSource

# Shared column names used in tests
DEFAULT_NAMES = [
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width",
    "target",
]


# Common mock datasets used across tests
MOCK_SMALL = {
    "sepal_length": [5.1, 4.9],
    "sepal_width": [3.5, 3.0],
    "petal_length": [1.4, 1.4],
    "petal_width": [0.2, 0.2],
    "target": [0, 0],
}

MOCK_STANDARD = {
    "sepal_length": [5.1, 4.9, 4.7],
    "sepal_width": [3.5, 3.0, 3.2],
    "petal_length": [1.4, 1.4, 1.3],
    "petal_width": [0.2, 0.2, 0.2],
    "target": [0, 0, 0],
}


@pytest.fixture
def df_factory(monkeypatch):
    """Return a factory that builds a `DataFrame` instance
       with a mocked `pandas.read_csv`.

    Usage: df = df_factory(mock_data)
    """

    def _make(mock_data):
        monkeypatch.setattr(pd, "read_csv", lambda *a, **k: pd.DataFrame(mock_data))
        return PandasSource(
            file_path="dummy.csv",
            separator=",",
            decimal=".",
            header=False,
            names=DEFAULT_NAMES,
        )

    return _make


def test_dataframe_loads_csv(df_factory):
    df = df_factory(MOCK_SMALL)
    assert df.df.equals(pd.DataFrame(MOCK_SMALL))


def test_dataframe_head(df_factory):
    df = df_factory(MOCK_STANDARD)
    assert df.head(2).equals(pd.DataFrame(MOCK_STANDARD).head(2))


def test_dataframe_tail(df_factory):
    df = df_factory(MOCK_STANDARD)
    assert df.tail(2).equals(pd.DataFrame(MOCK_STANDARD).tail(2))


def test_dataframe_describe(df_factory):
    df = df_factory(MOCK_STANDARD)
    assert df.describe().equals(pd.DataFrame(MOCK_STANDARD).describe())


def test_metadata(df_factory):
    df = df_factory(MOCK_STANDARD)
    metadata = df.metadata
    assert metadata["columns"] == DEFAULT_NAMES
    assert metadata["shape"] == (3, 5)
    assert "dtypes" in metadata


# Tests for URL functionality
@patch("src.data.sources.pandas_source.is_url")
@patch("src.data.sources.pandas_source.CacheManager")
@patch("src.data.sources.pandas_source.get_cached_file_path")
@patch("pandas.read_csv")
def test_url_source_initialization(
    mock_read_csv, mock_get_cached_path, mock_cache_manager, mock_is_url
):
    """Test that URL sources are properly initialized with cache manager."""
    # Setup mocks
    mock_is_url.return_value = True
    mock_cache_path = Path("/cache/test.csv")
    mock_get_cached_path.return_value = mock_cache_path
    mock_cache_instance = MagicMock()
    mock_cache_manager.return_value = mock_cache_instance
    mock_read_csv.return_value = pd.DataFrame(MOCK_SMALL)

    # Create PandasSource with URL
    test_url = "https://example.com/data.csv"
    source = PandasSource(test_url, names=DEFAULT_NAMES)

    # Verify URL detection and cache manager setup
    mock_is_url.assert_called_once_with(test_url)
    mock_cache_manager.assert_called_once()
    mock_cache_instance.ensure_file_cached.assert_called_once_with(
        test_url, mock_cache_path
    )

    assert source.is_url is True
    assert source.cache_manager is mock_cache_instance
    assert source.original_source == test_url


@patch("src.data.sources.pandas_source.is_url")
@patch("pandas.read_csv")
def test_local_file_initialization(mock_read_csv, mock_is_url):
    """Test that local files are properly initialized without cache manager."""
    # Setup mocks
    mock_is_url.return_value = False
    mock_read_csv.return_value = pd.DataFrame(MOCK_SMALL)

    # Create PandasSource with local file
    test_path = "local/file.csv"
    source = PandasSource(test_path, names=DEFAULT_NAMES)

    # Verify local file setup
    mock_is_url.assert_called_once_with(test_path)
    assert source.is_url is False
    assert source.cache_manager is None
    assert isinstance(source.file_path, Path)


def test_metadata_for_url_source(df_factory):
    """Test metadata includes URL-specific fields for URL sources."""
    # Create a source and manually set it as URL source
    source = df_factory(MOCK_STANDARD)
    source.is_url = True
    source.cache_dir = Path("/test/cache")

    metadata = source.metadata
    assert metadata["source_type"] == "url"
    assert "cache_dir" in metadata
    assert "is_cached" in metadata


def test_metadata_for_local_file(df_factory):
    """Test metadata for local file sources."""
    source = df_factory(MOCK_STANDARD)
    # Ensure it's treated as local file (default behavior)
    source.is_url = False

    metadata = source.metadata
    assert metadata["source_type"] == "local_file"
    assert "cache_dir" not in metadata
    assert "is_cached" not in metadata


def test_refresh_cache_raises_error_for_local_files(df_factory):
    """Test that refresh_cache raises ValueError for local files."""
    source = df_factory(MOCK_STANDARD)
    source.is_url = False  # Ensure it's treated as local file

    with pytest.raises(ValueError, match="Cannot refresh cache for local file sources"):
        source.refresh_cache()


@patch("src.data.sources.pandas_source.is_url")
@patch("src.data.sources.pandas_source.CacheManager")
@patch("src.data.sources.pandas_source.get_cached_file_path")
@patch("pandas.read_csv")
def test_refresh_cache_for_url_source(
    mock_read_csv, mock_get_cached_path, mock_cache_manager, mock_is_url
):
    """Test refresh_cache functionality for URL sources."""
    # Setup mocks
    mock_is_url.return_value = True
    mock_cache_path = Path("/cache/test.csv")
    mock_get_cached_path.return_value = mock_cache_path
    mock_cache_instance = MagicMock()
    mock_cache_manager.return_value = mock_cache_instance
    mock_read_csv.return_value = pd.DataFrame(MOCK_SMALL)

    # Create URL source
    test_url = "https://example.com/data.csv"
    source = PandasSource(test_url, names=DEFAULT_NAMES)

    # Test refresh_cache
    with patch("builtins.print"):  # Mock print to avoid output in tests
        source.refresh_cache()

    # Verify cache operations
    mock_cache_instance.remove_cached_file.assert_called_with(mock_cache_path)
    assert (
        mock_cache_instance.ensure_file_cached.call_count == 2
    )  # Once in init, once in refresh


def test_constructor_with_path_object():
    """Test constructor works with Path objects."""
    with patch("pandas.read_csv") as mock_read_csv:
        mock_read_csv.return_value = pd.DataFrame(MOCK_SMALL)

        path_obj = Path("test/file.csv")
        source = PandasSource(path_obj, names=DEFAULT_NAMES)

        assert isinstance(source.file_path, Path)
        assert source.original_source == str(path_obj)
