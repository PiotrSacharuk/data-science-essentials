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
