from unittest.mock import patch

import pandas as pd

from source.pandas_utils.read_data import DataFrame


# Mock pandas.read_csv to simulate loading data
@patch("pandas.read_csv")
def test_dataframe_loads_csv(mock_read_csv):
    # Prepare mock data
    mock_data = {
        "sepal_length": [5.1, 4.9],
        "sepal_width": [3.5, 3.0],
        "petal_length": [1.4, 1.4],
        "petal_width": [0.2, 0.2],
        "target": [0, 0],
    }
    mock_read_csv.return_value = pd.DataFrame(mock_data)

    # Test the DataFrame class
    df = DataFrame(
        file_path="dummy.csv",
        separator=",",
        decimal=".",
        header=False,
        names=["sepal_length", "sepal_width", "petal_length", "petal_width", "target"],
    )
    assert df.df.equals(pd.DataFrame(mock_data))  # Verify the data is correct


@patch("pandas.read_csv")
def test_dataframe_head(mock_read_csv):
    # Prepare mock data
    mock_data = {
        "sepal_length": [5.1, 4.9, 4.7],
        "sepal_width": [3.5, 3.0, 3.2],
        "petal_length": [1.4, 1.4, 1.3],
        "petal_width": [0.2, 0.2, 0.2],
        "target": [0, 0, 0],
    }
    mock_read_csv.return_value = pd.DataFrame(mock_data)

    # Test the head method
    df = DataFrame(
        file_path="dummy.csv",
        separator=",",
        decimal=".",
        header=False,
        names=["sepal_length", "sepal_width", "petal_length", "petal_width", "target"],
    )
    assert df.head(2).equals(pd.DataFrame(mock_data).head(2))


@patch("pandas.read_csv")
def test_dataframe_tail(mock_read_csv):
    # Prepare mock data
    mock_data = {
        "sepal_length": [5.1, 4.9, 4.7],
        "sepal_width": [3.5, 3.0, 3.2],
        "petal_length": [1.4, 1.4, 1.3],
        "petal_width": [0.2, 0.2, 0.2],
        "target": [0, 0, 0],
    }
    mock_read_csv.return_value = pd.DataFrame(mock_data)

    # Test the tail method
    df = DataFrame(
        file_path="dummy.csv",
        separator=",",
        decimal=".",
        header=False,
        names=["sepal_length", "sepal_width", "petal_length", "petal_width", "target"],
    )
    assert df.tail(2).equals(pd.DataFrame(mock_data).tail(2))


@patch("pandas.read_csv")
def test_dataframe_describe(mock_read_csv):
    # Prepare mock data
    mock_data = {
        "sepal_length": [5.1, 4.9, 4.7],
        "sepal_width": [3.5, 3.0, 3.2],
        "petal_length": [1.4, 1.4, 1.3],
        "petal_width": [0.2, 0.2, 0.2],
        "target": [0, 0, 0],
    }
    mock_read_csv.return_value = pd.DataFrame(mock_data)

    # Test the describe method
    df = DataFrame(
        file_path="dummy.csv",
        separator=",",
        decimal=".",
        header=False,
        names=["sepal_length", "sepal_width", "petal_length", "petal_width", "target"],
    )
    assert df.describe().equals(pd.DataFrame(mock_data).describe())
