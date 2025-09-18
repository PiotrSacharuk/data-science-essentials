import pandas as pd


class DataFrame:
    def __init__(self, file_path, separator=",", decimal=".", header=False, names=None):
        self.file_path = file_path
        self.separator = separator
        self.decimal = decimal
        self.header = header
        self.names = names if names is not None else []
        self.df = self.read_csv_file()

    def read_csv_file(self) -> pd.DataFrame:
        """
        Reads a CSV file and returns a pandas DataFrame using instance attributes.
        """
        return pd.read_csv(
            self.file_path,
            sep=self.separator,
            decimal=self.decimal,
            header=0 if self.header else None,
            names=self.names if not self.header else None,
        )

    def head(self, n=5):
        return self.df.head(n)

    def tail(self, n=5):
        return self.df.tail(n)

    def describe(self):
        return self.df.describe()
