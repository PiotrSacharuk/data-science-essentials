"""
Test configuration for pytest.

This file is automatically loaded by pytest and provides configuration
for all tests in the project.

Security Note: This file contains HTTP URLs for testing purposes only.
These URLs are not used for actual network connections and are safe.
SonarQube security warnings about HTTP usage can be ignored in test files.
"""

import os
import sys

# Add the project root directory to Python path to ensure imports work correctly
# This ensures that 'import src.data' works in all tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

# Test URL constants for consistent URL usage across tests
TEST_DOMAIN = "example.com"
TEST_URL_BASE = f"https://{TEST_DOMAIN}"
TEST_FILE_NAME = "data.csv"
TEST_URL_FULL = f"{TEST_URL_BASE}/{TEST_FILE_NAME}"
TEST_URL_WITH_QUERY = f"{TEST_URL_FULL}?query=value"
TEST_URL_INVALID = "https://invalid-domain-xyz-12345.com/file.csv"

# Test subdomain URL for specific test cases
TEST_URL_SUBDOMAIN = f"https://sub.{TEST_DOMAIN}/path"

# Additional URL constants for comprehensive testing
# nosec: B104 - HTTP needed for testing URL scheme validation
TEST_URL_HTTP = f"http://{TEST_DOMAIN}"  # nosec: B104
TEST_URL_JSON = f"{TEST_URL_BASE}/data.json"
TEST_URL_PLAIN = f"{TEST_URL_BASE}/data"
TEST_URL_SPECIAL_CHARS = f"{TEST_URL_BASE}/data with spaces.csv?param=value&other=123"

# Test URLs with different schemes
# nosec: B601 - Test URL only, not used for actual connections
TEST_URL_FTP = f"ftp://{TEST_DOMAIN}"  # nosec: B601
TEST_URL_MAILTO = f"mailto:test@{TEST_DOMAIN}"
TEST_URL_FILE = "file:///path/to/file"

# Malformed URLs for testing (used to verify error handling)
TEST_URL_MALFORMED_EMPTY = ""
TEST_URL_MALFORMED_INVALID = "not-a-url"
# nosec: B104 - Malformed URL for testing, not used for connections
TEST_URL_MALFORMED_NO_NETLOC = "http://"  # nosec: B104
TEST_URL_MALFORMED_NO_SCHEME = f"://{TEST_DOMAIN}"

# External domains for testing
TEST_EXTERNAL_DOMAIN1 = "google.com"
TEST_EXTERNAL_DOMAIN2 = "github.com"
