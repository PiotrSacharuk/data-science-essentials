from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd


class PandasSource:
    """
    A utility class for reading and processing CSV files using pandas.

    This class provides a convenient interface for loading CSV data with
    configurable parameters and basic data exploration methods.

    Attributes:
        file_path (str or Path): Path to the CSV file
        separator (str): Column separator character
        decimal (str): Decimal point character
        header (bool): Whether the file has a header row
        names (List[str]): Column names to use
        df (pd.DataFrame): The loaded DataFrame
    """

    def __init__(
        self,
        file_path: Union[str, Path],
        separator: str = ",",
        decimal: str = ".",
        header: bool = False,
        names: Optional[List[str]] = None,
    ):
        """
        Initialize PandasSource with CSV file parameters.

        Args:
            file_path (str or Path): Path to the CSV file to read
            separator (str, optional): Field delimiter. Defaults to ",".
            decimal (str, optional): Character used as decimal point. Defaults to ".".
            header (bool, optional): Whether file has column headers. Defaults to False.
            names (List[str], optional): List of column names to use. Defaults to None.
        """
        self.file_path = Path(file_path) if isinstance(file_path, str) else file_path
        self.separator = separator
        self.decimal = decimal
        self.header = header
        self.names = names if names is not None else []
        self.df = self.read_csv_file()

    def read_csv_file(self) -> pd.DataFrame:
        """
        Read CSV file and return pandas DataFrame using instance attributes.

        Returns:
            pd.DataFrame: The loaded data as a pandas DataFrame

        Raises:
            FileNotFoundError: If the specified file doesn't exist
            pd.errors.EmptyDataError: If the file is empty
        """
        return pd.read_csv(
            self.file_path,
            sep=self.separator,
            decimal=self.decimal,
            header=0 if self.header else None,
            names=self.names if not self.header else None,
        )

    def head(self, n: int = 5) -> pd.DataFrame:
        """
        Return the first n rows of the DataFrame.

        Args:
            n (int, optional): Number of rows to return. Defaults to 5.

        Returns:
            pd.DataFrame: First n rows of the data
        """
        return self.df.head(n)

    def tail(self, n: int = 5) -> pd.DataFrame:
        """
        Return the last n rows of the DataFrame.

        Args:
            n (int, optional): Number of rows to return. Defaults to 5.

        Returns:
            pd.DataFrame: Last n rows of the data
        """
        return self.df.tail(n)

    def describe(self) -> pd.DataFrame:
        """
        Generate descriptive statistics for numerical columns.

        Returns:
            pd.DataFrame: Summary statistics including count, mean, std, min, max, etc.
        """
        return self.df.describe()

    @property
    def metadata(self) -> Dict[str, Any]:
        """
        Get metadata about the data source.

        Returns:
            Dict[str, Any]: A dictionary containing metadata about the data source.
        """
        return {
            "file_path": str(self.file_path),
            "separator": self.separator,
            "decimal": self.decimal,
            "header": self.header,
            "columns": list(self.df.columns),
            "shape": self.df.shape,
            "dtypes": {col: str(dtype) for col, dtype in self.df.dtypes.items()},
        }
