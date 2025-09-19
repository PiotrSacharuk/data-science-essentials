"""
Utility script to download the Iris dataset from UCI ML Repository.

This script downloads the classic Iris dataset and saves it as a local CSV file.
"""

import urllib.request
from pathlib import Path
from typing import Optional


def download_iris_dataset(
    url: Optional[str] = None, output_file: str = "iris.csv"
) -> bool:
    """
    Download the Iris dataset from UCI ML Repository.

    Args:
        url (str, optional): URL to download from. Uses default UCI URL if None.
        output_file (str, optional): Output filename. Defaults to "iris.csv".

    Returns:
        bool: True if download successful, False otherwise
    """
    if url is None:
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"

    try:
        print(f"Downloading dataset from: {url}")
        response = urllib.request.urlopen(url, timeout=10)
        data = response.read()

        output_path = Path(output_file)
        with open(output_path, "wb") as f:
            f.write(data)

        print(f"Dataset successfully downloaded to: {output_path.absolute()}")
        return True

    except Exception as e:
        print(f"Error downloading or saving the file: {e}")
        return False


if __name__ == "__main__":
    success = download_iris_dataset()
    if not success:
        exit(1)
