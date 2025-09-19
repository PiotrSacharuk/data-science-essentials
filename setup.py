#!/usr/bin/env python3
"""
Project Setup Script for Data Science Essentials

This script automatically creates the complete project structure and downloads
required datasets. Run this script after cloning the repository to set up
your development environment.

Usage:
    python setup.py
"""

import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Optional

import yaml


class ProjectSetup:
    """Handles complete project setup and initialization."""

    def __init__(self, project_root: Optional[Path] = None):
        """Initialize setup with project root directory."""
        self.project_root = project_root or Path(__file__).parent
        self.config = self._load_config()
        self.directories = self.config.get("directories", [])
        self.datasets = self.config.get("datasets", [])

    def _load_config(self) -> Any:
        """Load configuration from YAML file."""
        config_path = Path(os.path.join(self.project_root, "config.yaml"))

        # If config file doesn't exist, exit with error
        if not config_path.exists():
            print("Error: Configuration file not found.")
            print(f"Expected config file at: {config_path}")
            print("Please make sure config.yaml exists in the project root.")
            sys.exit(1)

        try:
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
                if not config:
                    print("Error: Empty configuration file.")
                    sys.exit(1)
                return config
        except Exception as e:
            print(f"Error loading configuration: {e}")
            sys.exit(1)

    def create_directories(self) -> None:
        """Create all required project directories."""
        print("Creating project directory structure...")

        for directory in self.directories:
            dir_path = Path(os.path.join(self.project_root, directory))
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  Created: {directory}")

        print(f"Created {len(self.directories)} directories")

    def download_dataset(self, dataset: dict) -> bool:
        """Download a single dataset."""
        url = dataset["url"]
        filename = dataset["filename"]
        destination = Path(os.path.join(self.project_root, dataset["destination"]))
        file_path = Path(os.path.join(destination, filename))

        # Create destination directory if it doesn't exist
        destination.mkdir(parents=True, exist_ok=True)

        # Skip if file already exists
        if file_path.exists():
            print(f"  {filename} already exists, skipping download")
            return True

        try:
            print(f"  Downloading {filename} from {url}")
            urllib.request.urlretrieve(url, file_path)

            # Verify file was downloaded
            if file_path.exists() and file_path.stat().st_size > 0:
                print(f"  Downloaded: {filename} ({file_path.stat().st_size} bytes)")
                return True
            else:
                print(f"  Download failed: {filename}")
                return False

        except urllib.error.URLError as e:
            print(f"  Download failed: {filename} - {e}")
            return False
        except Exception as e:
            print(f"  Unexpected error downloading {filename}: {e}")
            return False

    def download_datasets(self) -> None:
        """Download all required datasets."""
        print("Downloading datasets...")

        successful = 0
        total = len(self.datasets)

        for dataset in self.datasets:
            if self.download_dataset(dataset):
                successful += 1

        if successful == total:
            print(f"Successfully downloaded all {total} datasets")
        else:
            print(f"Downloaded {successful}/{total} datasets")

    def install_dependencies(self) -> None:
        """Install Python dependencies."""
        print("Installing Python dependencies...")

        try:
            import subprocess

            # Install main dependencies
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                print("  Installed main dependencies")
            else:
                print(f"  Failed to install dependencies: {result.stderr}")

        except Exception as e:
            print(f"  Error installing dependencies: {e}")

    def run_setup(self) -> None:
        """Run complete project setup."""
        print("Setting up Data Science Essentials project...")
        print(f"Project root: {self.project_root}")
        print(
            "Using configuration from: "
            f"{Path(os.path.join(self.project_root, 'config.yaml'))}"
        )
        print("=" * 50)

        try:
            self.create_directories()
            print()

            self.download_datasets()
            print()

            self.install_dependencies()
            print()

            print("=" * 50)
            print("Project setup completed successfully!")
            print()
            print("Next steps:")
            print("1. Activate your virtual environment:")
            print("   source .venv/bin/activate  # Linux/Mac")
            print("   .venv\\Scripts\\activate     # Windows")
            print()
            print("2. Start Jupyter Lab:")
            print("   python make.py notebook")
            print()
            print("3. To add more datasets, edit config.yaml")
            print()
            print("4. Run tests to verify everything works:")
            print("   python make.py test")

        except Exception as e:
            print(f"Setup failed: {e}")
            sys.exit(1)


def main():
    """Main entry point."""
    setup = ProjectSetup()
    setup.run_setup()


if __name__ == "__main__":
    main()
