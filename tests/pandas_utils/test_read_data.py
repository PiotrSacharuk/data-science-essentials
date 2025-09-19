"""
Tests for the PandasDataReader class in pandas_utils.read_data module.

This module contains comprehensive tests for CSV data reading functionality
including various configurations and edge cases.
"""

import pandas as pd
import pytest

from source.pandas_utils.read_data import PandasDataReader

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
        return PandasDataReader(
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
