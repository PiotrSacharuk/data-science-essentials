"""
Tests for the FastAPI server application in app.server module.
"""

import pytest
from fastapi.testclient import TestClient

from app.server import app


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app)


class TestAppInitialization:
    """Test FastAPI app initialization."""

    def test_app_creation(self):
        """Test that the app is a FastAPI instance."""
        assert app is not None
        assert hasattr(app, "routes")

    def test_app_has_pandas_router(self, client):
        """Test that the app includes the pandas router."""
        # Check if /data routes are registered
        routes = [route.path for route in app.routes]
        # Pandas router should have registered routes with /data prefix
        assert any(route.startswith("/data") for route in routes)


class TestAppRoutes:
    """Test that routes are properly mounted."""

    def test_openapi_schema(self, client):
        """Test that OpenAPI schema is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        assert "openapi" in response.json()

    def test_docs_available(self, client):
        """Test that API documentation is available."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_redoc_available(self, client):
        """Test that ReDoc documentation is available."""
        response = client.get("/redoc")
        assert response.status_code == 200


class TestAppHealthCheck:
    """Test basic app health checks."""

    def test_app_startup(self, client):
        """Test that app can handle requests after startup."""
        # Simple request to verify app is working
        # We'll use OpenAPI schema endpoint as a health check
        response = client.get("/openapi.json")
        assert response.status_code == 200

    def test_404_on_unknown_route(self, client):
        """Test that unknown routes return 404."""
        response = client.get("/unknown/route")
        assert response.status_code == 404
