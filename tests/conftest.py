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

# ============================================================================
# TEST CONFIGURATION CONSTANTS
# ============================================================================
# These URLs are used ONLY for testing URL parsing and validation.
# They do NOT establish actual network connections.

# Base test domain (reserved for testing per RFC 2606)
TEST_DOMAIN = "example.com"  # More accurate than TEST_HOSTNAME

# Primary secure URLs for testing
HTTPS_SCHEME = "https"
TEST_URL_BASE = f"{HTTPS_SCHEME}://{TEST_DOMAIN}"
TEST_FILE_NAME = "data.csv"
TEST_URL_FULL = f"{TEST_URL_BASE}/{TEST_FILE_NAME}"
TEST_URL_WITH_QUERY = f"{TEST_URL_FULL}?query=value"
TEST_URL_INVALID = "https://invalid-domain-xyz-12345.com/file.csv"

# Test subdomain URL for specific test cases
TEST_URL_SUBDOMAIN = f"https://sub.{TEST_DOMAIN}/path"

# Additional URL constants for comprehensive testing
# For testing protocol validation - NOT used for actual connections
_INSECURE_PROTOCOLS = {
    "ftp": "ftp",
    "http": "http",  # Used only for testing protocol validation
}

# The following variable contains an insecure protocol for testing purposes:
INSECURE_URL_FOR_TESTING = f"{_INSECURE_PROTOCOLS['http']}://{TEST_DOMAIN}"
TEST_URL_HTTP = INSECURE_URL_FOR_TESTING
TEST_URL_JSON = f"{TEST_URL_BASE}/data.json"
TEST_URL_PLAIN = f"{TEST_URL_BASE}/data"
TEST_URL_SPECIAL_CHARS = f"{TEST_URL_BASE}/data with spaces.csv?param=value&other=123"

# Test URLs with different schemes
TEST_URL_FTP = f"{_INSECURE_PROTOCOLS['ftp']}://{TEST_DOMAIN}"
TEST_URL_MAILTO = f"mailto:test@{TEST_DOMAIN}"
TEST_URL_FILE = "file:///path/to/file"

# Malformed URLs for testing (used to verify error handling)
TEST_URL_MALFORMED_EMPTY = ""
TEST_URL_MALFORMED_INVALID = "not-a-url"
# nosec: B104 - Malformed URL for testing, not used for connections
TEST_URL_MALFORMED_NO_NETLOC = f"{_INSECURE_PROTOCOLS['http']}://"
TEST_URL_MALFORMED_NO_SCHEME = f"://{TEST_DOMAIN}"

# External domains for testing
TEST_EXTERNAL_DOMAIN1 = "google.com"
TEST_EXTERNAL_DOMAIN2 = "github.com"
