"""
Utility script to download the Iris dataset from UCI ML Repository.

This script downloads the classic Iris dataset and saves it as a local CSV file.
"""

import os
import urllib.request
from pathlib import Path
from typing import Optional


def download_iris_dataset(
    url: Optional[str] = None, output_dir: str = "data/raw", filename: str = "iris.csv"
) -> bool:
    """
    Download the Iris dataset from UCI ML Repository.

    Args:
        url (str, optional): URL to download from. Uses default UCI URL if None.
        output_dir (str, optional): Output directory. Defaults to "data/raw".
        filename (str, optional): Output filename. Defaults to "iris.csv".

    Returns:
        bool: True if download successful, False otherwise
    """
    if url is None:
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"

    try:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        file_path = Path(os.path.join(output_path, filename))

        if file_path.exists():
            print(f"File already exists: {file_path.absolute()}")
            return True

        print(f"Downloading dataset from: {url}")
        response = urllib.request.urlopen(url, timeout=10)
        data = response.read()

        with open(file_path, "wb") as f:
            f.write(data)

        print(f"Dataset successfully downloaded to: {file_path.absolute()}")
        print(f"File size: {file_path.stat().st_size} bytes")
        return True

    except Exception as e:
        print(f"Error downloading or saving the file: {e}")
        return False


if __name__ == "__main__":
    success = download_iris_dataset()
    if not success:
        exit(1)
