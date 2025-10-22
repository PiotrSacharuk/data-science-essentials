"""
Tests for the Pandas routes in app.routes.pandas module.
"""

import tempfile
from http import HTTPStatus
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.server import app


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def sample_csv_path():
    """Create a sample CSV file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("name,age,city\n")
        f.write("Alice,30,NYC\n")
        f.write("Bob,25,LA\n")
        f.write("Charlie,35,Chicago\n")
        path = f.name
    yield path
    # Cleanup
    Path(path).unlink()


@pytest.fixture
def iris_csv_url():
    """Provide a URL to the Iris dataset."""
    return (
        "https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv"
    )


class TestLoadDataEndpoint:
    """Test POST /data/load endpoint."""

    def test_load_data_with_local_file(self, client, sample_csv_path):
        """Test loading data from a local file URL."""
        request_data = {
            "source_url": f"file://{sample_csv_path}",
            "separator": ",",
            "header": True,
        }
        response = client.post("/data/load", json=request_data)

        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["status"] == "success"
        assert data["shape"] == [3, 3]  # Shape is returned as list in JSON
        assert set(data["columns"]) == {"name", "age", "city"}
        assert len(data["preview"]) == 3

    def test_load_data_invalid_url(self, client):
        """Test loading data with invalid URL."""
        request_data = {
            "source_url": "http://invalid-domain-xyz-12345.com/file.csv",
            "separator": ",",
            "header": True,
        }
        response = client.post("/data/load", json=request_data)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        data = response.json()
        assert "detail" in data

    def test_load_data_custom_separator(self, client):
        """Test loading data with custom separator."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("name;age;city\n")
            f.write("Alice;30;NYC\n")
            f.write("Bob;25;LA\n")
            path = f.name

        try:
            request_data = {
                "source_url": f"file://{path}",
                "separator": ";",
                "header": True,
            }
            response = client.post("/data/load", json=request_data)

            assert response.status_code == HTTPStatus.OK
            data = response.json()
            assert set(data["columns"]) == {"name", "age", "city"}
        finally:
            Path(path).unlink()

    def test_load_data_missing_source_url(self, client):
        """Test loading data without source_url (required field)."""
        request_data = {"separator": ",", "header": True}
        response = client.post("/data/load", json=request_data)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_load_data_default_parameters(self, client, sample_csv_path):
        """Test loading data with default parameters."""
        request_data = {"source_url": f"file://{sample_csv_path}"}
        response = client.post("/data/load", json=request_data)

        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["status"] == "success"


class TestHeadEndpoint:
    """Test POST /data/head endpoint."""

    def test_head_default_rows(self, client, sample_csv_path):
        """Test getting first 5 rows (default)."""
        request_data = {"source_url": f"file://{sample_csv_path}"}
        response = client.post("/data/head", json=request_data)

        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["status"] == "success"
        assert len(data["data"]) == 3  # File has only 3 rows

    def test_head_custom_n(self, client, sample_csv_path):
        """Test getting first N rows."""
        request_data = {"source_url": f"file://{sample_csv_path}", "n": 2}
        response = client.post("/data/head", json=request_data)

        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert len(data["data"]) == 2
        assert data["data"][0]["name"] == "Alice"
        assert data["data"][1]["name"] == "Bob"

    def test_head_n_larger_than_rows(self, client, sample_csv_path):
        """Test getting more rows than available."""
        request_data = {"source_url": f"file://{sample_csv_path}", "n": 10}
        response = client.post("/data/head", json=request_data)

        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert len(data["data"]) == 3  # Only 3 rows available


class TestTailEndpoint:
    """Test POST /data/tail endpoint."""

    def test_tail_default_rows(self, client, sample_csv_path):
        """Test getting last 5 rows (default)."""
        request_data = {"source_url": f"file://{sample_csv_path}"}
        response = client.post("/data/tail", json=request_data)

        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["status"] == "success"
        assert len(data["data"]) == 3

    def test_tail_custom_n(self, client, sample_csv_path):
        """Test getting last N rows."""
        request_data = {"source_url": f"file://{sample_csv_path}", "n": 2}
        response = client.post("/data/tail", json=request_data)

        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert len(data["data"]) == 2
        assert data["data"][0]["name"] == "Bob"
        assert data["data"][1]["name"] == "Charlie"

    def test_tail_n_larger_than_rows(self, client, sample_csv_path):
        """Test getting more rows than available."""
        request_data = {"source_url": f"file://{sample_csv_path}", "n": 10}
        response = client.post("/data/tail", json=request_data)

        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert len(data["data"]) == 3


class TestDescribeEndpoint:
    """Test POST /data/describe endpoint."""

    def test_describe_statistics(self, client, sample_csv_path):
        """Test getting statistical summary of data."""
        request_data = {"source_url": f"file://{sample_csv_path}"}
        response = client.post("/data/describe", json=request_data)

        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["status"] == "success"
        assert "statistics" in data
        # Age column should have statistics (it's numeric)
        assert "age" in data["statistics"]

    def test_describe_numeric_columns(self, client, sample_csv_path):
        """Test that numeric columns have proper statistics."""
        request_data = {"source_url": f"file://{sample_csv_path}"}
        response = client.post("/data/describe", json=request_data)

        assert response.status_code == HTTPStatus.OK
        data = response.json()
        stats = data["statistics"]["age"]
        # Statistics should have count, mean, std, min, max, etc.
        assert "count" in stats or "50%" in stats or "mean" in stats


class TestEndpointErrorHandling:
    """Test error handling across endpoints."""

    def test_all_endpoints_handle_invalid_file(self, client):
        """Test that all endpoints handle file not found gracefully."""
        request_data = {"source_url": "file:///nonexistent/path/file.csv"}

        endpoints = ["/data/load", "/data/head", "/data/tail", "/data/describe"]

        for endpoint in endpoints:
            response = client.post(endpoint, json=request_data)
            assert (
                response.status_code == HTTPStatus.BAD_REQUEST
            ), f"Failed for {endpoint}"

    def test_request_validation_missing_url(self, client):
        """Test that requests without URL are rejected."""
        request_data = {}

        response = client.post("/data/load", json=request_data)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
