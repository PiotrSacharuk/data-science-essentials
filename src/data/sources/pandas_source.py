from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd

from src.utils.cache.cache_manager import CacheManager
from src.utils.network.url_utils import get_cached_file_path, is_url


class PandasSource:
    """
    A utility class for reading and processing CSV files using pandas.

    This class provides a convenient interface for loading CSV data with
    configurable parameters and basic data exploration methods.
    Supports both local files and remote URLs with automatic caching.

    Attributes:
        original_source (str): Original file path or URL
        separator (str): Column separator character
        decimal (str): Decimal point character
        header (bool): Whether the file has a header row
        names (List[str]): Column names to use
        df (pd.DataFrame): The loaded DataFrame
        is_url (bool): Whether the source is a URL
        cache_manager (Optional[CacheManager]): Cache manager for URL sources,
                                                None for local files
    """

    # Type annotations for instance attributes
    cache_manager: Optional[CacheManager]

    def __init__(
        self,
        file_path: Union[str, Path],
        separator: str = ",",
        decimal: str = ".",
        header: bool = False,
        names: Optional[List[str]] = None,
        cache_dir: str = "data/cache",
        timeout: int = 30,
    ):
        """
        Initialize PandasSource with CSV file parameters.

        Args:
            file_path (str or Path): Path to the CSV file or URL
            separator (str, optional): Field delimiter. Defaults to ",".
            decimal (str, optional): Character used as decimal point. Defaults to ".".
            header (bool, optional): Whether file has column headers. Defaults to False.
            names (List[str], optional): List of column names to use. Defaults to None.
            cache_dir (str, optional): Directory for caching downloaded files.
                                       Defaults to "data/cache".
            timeout (int, optional): Timeout for URL downloads in seconds.
                                      Defaults to 30.
        """
        self.original_source = str(file_path)
        self.separator = separator
        self.decimal = decimal
        self.header = header
        self.names = names if names is not None else []
        self.cache_dir = Path(cache_dir)
        self.timeout = timeout
        self.is_url = is_url(self.original_source)

        # Initialize cache manager for URL sources
        if self.is_url:
            self.cache_manager = CacheManager(self.cache_dir, self.timeout)
            self.file_path = get_cached_file_path(self.original_source, self.cache_dir)
            self.cache_manager.ensure_file_cached(self.original_source, self.file_path)
        else:
            self.cache_manager = None
            self.file_path = (
                Path(file_path) if isinstance(file_path, str) else file_path
            )

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
        metadata = {
            "original_source": self.original_source,
            "source_type": "url" if self.is_url else "local_file",
            "file_path": str(self.file_path),
            "separator": self.separator,
            "decimal": self.decimal,
            "header": self.header,
            "columns": list(self.df.columns),
            "shape": self.df.shape,
            "dtypes": {col: str(dtype) for col, dtype in self.df.dtypes.items()},
        }

        if self.is_url:
            metadata["cache_dir"] = str(self.cache_dir)
            metadata["is_cached"] = self.file_path.exists()

        return metadata

    def refresh_cache(self) -> None:
        """
        Force refresh the cached data from URL.
        Only works for URL sources.

        Raises:
            ValueError: If the source is not a URL
        """
        if not self.is_url:
            raise ValueError("Cannot refresh cache for local file sources")

        if self.cache_manager:
            # Remove cached file and re-download
            self.cache_manager.remove_cached_file(self.file_path)
            self.cache_manager.ensure_file_cached(self.original_source, self.file_path)
            self.df = self.read_csv_file()
            print(f"Cache refreshed for: {self.original_source}")
