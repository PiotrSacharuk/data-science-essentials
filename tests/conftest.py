"""
Test configuration for pytest.

This file is automatically loaded by pytest and provides configuration
for all tests in the project.
"""

import os
import sys

# Add the project root directory to Python path to ensure imports work correctly
# This ensures that 'import src.data' works in all tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

# Test URL constants for consistent URL usage across tests
TEST_URL_BASE = "https://example.com"
TEST_URL_PATH = "/data.csv"
TEST_URL_FULL = f"{TEST_URL_BASE}{TEST_URL_PATH}"
TEST_URL_WITH_QUERY = f"{TEST_URL_FULL}?query=value"
TEST_URL_INVALID = "https://invalid-domain-xyz-12345.com/file.csv"

# Test subdomain URL for specific test cases
TEST_URL_SUBDOMAIN = "https://sub.example.com/path"
