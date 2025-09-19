"""
Data readers for various file formats and data sources.

This module provides convenient classes and functions for reading
CSV data, JSON, and other data formats using pandas and other libraries.
"""

from .pandas_data_reader import PandasDataReader

__all__ = ["PandasDataReader"]
__version__ = "0.1.0"
