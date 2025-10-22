"""
Tests for the Pandas routes in app.routes.pandas module.
"""

import tempfile
from http import HTTPStatus
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.server import app


@pytest.fixture
def client() -> TestClient:
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app)


def create_csv_file(content: str, suffix: str = ".csv") -> Generator[str, None, None]:
    """Helper to create temporary CSV files.

    Args:
        content: CSV content to write
        suffix: File suffix (default: .csv)

    Yields:
        Path to temporary file, cleaned up after use
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=suffix, delete=False) as f:
        f.write(content)
        path = f.name
    yield path
    Path(path).unlink()


@pytest.fixture
def sample_csv_path() -> Generator[str, None, None]:
    """Provide path to sample CSV file with default separator."""
    content = "name,age,city\nAlice,30,NYC\nBob,25,LA\nCharlie,35,Chicago\n"
    yield from create_csv_file(content)


@pytest.fixture
def sample_csv_semicolon() -> Generator[str, None, None]:
    """Provide path to sample CSV file with semicolon separator."""
    content = "name;age;city\nAlice;30;NYC\nBob;25;LA\n"
    yield from create_csv_file(content)


def assert_success_response(response, status_code: HTTPStatus = HTTPStatus.OK) -> dict:
    """Assert successful response and return data.

    Args:
        response: FastAPI test response
        status_code: Expected HTTP status code

    Returns:
        Response JSON data
    """
    assert response.status_code == status_code
    data = response.json()
    if status_code == HTTPStatus.OK:
        assert data["status"] == "success"
    return data


class TestLoadDataEndpoint:
    """Test POST /data/load endpoint."""

    def test_load_data_with_local_file(self, client, sample_csv_path):
        """Test loading data from a local file URL."""
        request_data = {"source_url": f"file://{sample_csv_path}"}
        response = client.post("/data/load", json=request_data)

        data = assert_success_response(response)
        assert data["shape"] == [3, 3]
        assert set(data["columns"]) == {"name", "age", "city"}
        assert len(data["preview"]) == 3

    def test_load_data_invalid_url(self, client):
        """Test loading data with invalid URL."""
        request_data = {"source_url": "http://invalid-domain-xyz-12345.com/file.csv"}
        response = client.post("/data/load", json=request_data)
        assert_success_response(response, HTTPStatus.BAD_REQUEST)

    def test_load_data_custom_separator(self, client, sample_csv_semicolon):
        """Test loading data with custom separator."""
        request_data = {
            "source_url": f"file://{sample_csv_semicolon}",
            "separator": ";",
        }
        response = client.post("/data/load", json=request_data)

        data = assert_success_response(response)
        assert set(data["columns"]) == {"name", "age", "city"}

    def test_load_data_missing_source_url(self, client):
        """Test loading data without source_url (required field)."""
        response = client.post("/data/load", json={})
        assert_success_response(response, HTTPStatus.UNPROCESSABLE_ENTITY)

    def test_load_data_default_parameters(self, client, sample_csv_path):
        """Test loading data with default parameters."""
        request_data = {"source_url": f"file://{sample_csv_path}"}
        response = client.post("/data/load", json=request_data)
        assert_success_response(response)


class TestSliceEndpoints:
    """Test /data/head and /data/tail endpoints."""

    @pytest.mark.parametrize("endpoint", ["/data/head", "/data/tail"])
    def test_default_rows(self, client, sample_csv_path, endpoint):
        """Test getting rows with default n=5."""
        response = client.post(
            endpoint, json={"source_url": f"file://{sample_csv_path}"}
        )
        data = assert_success_response(response)
        assert len(data["data"]) == 3  # File has only 3 rows

    @pytest.mark.parametrize(
        "endpoint,expected_first,expected_second",
        [
            ("/data/head", "Alice", "Bob"),
            ("/data/tail", "Bob", "Charlie"),
        ],
    )
    def test_custom_n(
        self, client, sample_csv_path, endpoint, expected_first, expected_second
    ):
        """Test getting N specific rows from head/tail."""
        response = client.post(
            endpoint, json={"source_url": f"file://{sample_csv_path}", "n": 2}
        )
        data = assert_success_response(response)
        assert len(data["data"]) == 2
        assert data["data"][0]["name"] == expected_first
        assert data["data"][1]["name"] == expected_second

    @pytest.mark.parametrize("endpoint", ["/data/head", "/data/tail"])
    def test_n_larger_than_rows(self, client, sample_csv_path, endpoint):
        """Test requesting more rows than available."""
        response = client.post(
            endpoint, json={"source_url": f"file://{sample_csv_path}", "n": 10}
        )
        data = assert_success_response(response)
        assert len(data["data"]) == 3


class TestDescribeEndpoint:
    """Test POST /data/describe endpoint."""

    def test_describe_statistics(self, client, sample_csv_path):
        """Test getting statistical summary of data."""
        response = client.post(
            "/data/describe", json={"source_url": f"file://{sample_csv_path}"}
        )
        data = assert_success_response(response)
        assert "statistics" in data
        assert "age" in data["statistics"]

    def test_describe_numeric_columns(self, client, sample_csv_path):
        """Test that numeric columns have statistics."""
        response = client.post(
            "/data/describe", json={"source_url": f"file://{sample_csv_path}"}
        )
        data = assert_success_response(response)
        stats = data["statistics"]["age"]
        assert any(key in stats for key in ["count", "50%", "mean"])


class TestEndpointErrorHandling:
    """Test error handling across endpoints."""

    @pytest.mark.parametrize(
        "endpoint",
        ["/data/load", "/data/head", "/data/tail", "/data/describe"],
    )
    def test_all_endpoints_handle_invalid_file(self, client, endpoint):
        """Test that all endpoints handle missing files gracefully."""
        response = client.post(
            endpoint, json={"source_url": "file:///nonexistent/path/file.csv"}
        )
        assert_success_response(response, HTTPStatus.BAD_REQUEST)

    def test_request_validation_missing_url(self, client):
        """Test that requests without URL are rejected."""
        response = client.post("/data/load", json={})
        assert_success_response(response, HTTPStatus.UNPROCESSABLE_ENTITY)
