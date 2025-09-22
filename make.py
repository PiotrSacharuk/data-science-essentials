#!/usr/bin/env python3
"""
Project Management Script for Data Science Essentials

This script provides common development tasks and utilities.
Think of it as a Python equivalent to Makefile.

Usage:
    python make.py <command> [options]

Commands:
    setup       - Set up project structure and download data
    install     - Install dependencies
    test        - Run tests
    test-cov    - Run tests with coverage
    clean       - Clean temporary files
    data        - Download datasets
    notebook    - Start Jupyter Lab
    help        - Show this help message

Examples:
    python make.py setup
    python make.py test-cov
    python make.py notebook
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


class ProjectManager:
    """Manages common development tasks for the project."""

    def __init__(self, project_root: Optional[Path] = None):
        """Initialize project manager."""
        self.project_root = project_root or Path(__file__).parent
        self.python = sys.executable

    def run_command(
        self, cmd: List[str], check: bool = True
    ) -> subprocess.CompletedProcess:
        """Run a shell command."""
        print(f"Running: {' '.join(cmd)}")
        return subprocess.run(cmd, check=check, cwd=self.project_root)

    def setup(self) -> None:
        """Set up project structure and download data."""
        print("Setting up project...")
        setup_script = self.project_root / "setup.py"
        if setup_script.exists():
            self.run_command([self.python, str(setup_script)])
        else:
            print("setup.py not found!")
            sys.exit(1)

    def install(self) -> None:
        """Install dependencies."""
        print("Installing dependencies...")
        requirements_files = ["requirements.txt"]

        for req_file in requirements_files:
            req_path = self.project_root / req_file
            if req_path.exists():
                self.run_command(
                    [self.python, "-m", "pip", "install", "-r", str(req_path)]
                )
            else:
                print(f"{req_file} not found!")
                sys.exit(1)

    def test(self, coverage: bool = False) -> None:
        """Run tests."""
        cmd = [self.python, "-m", "pytest", "tests/"]

        if coverage:
            print("Running tests with coverage...")
            cmd.extend(
                ["--cov=source", "--cov-report=term-missing", "--cov-report=html"]
            )
        else:
            print("Running tests...")
            cmd.append("-v")

        # Set PYTHONPATH
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.project_root)

        subprocess.run(cmd, env=env, cwd=self.project_root, check=True)

    def clean(self) -> None:
        """Clean temporary files."""
        print("Cleaning temporary files...")

        patterns = [
            "**/__pycache__",
            "**/*.pyc",
            "**/*.pyo",
            "**/*.pyd",
            ".pytest_cache",
            ".mypy_cache",
            ".coverage",
            "htmlcov",
            "dist",
            "build",
            "*.egg-info",
            ".ipynb_checkpoints",
        ]

        cleaned = 0
        for pattern in patterns:
            for path in self.project_root.glob(pattern):
                if path.is_dir():
                    shutil.rmtree(path)
                    print(f"  Removed directory: {path}")
                elif path.is_file():
                    path.unlink()
                    print(f"  Removed file: {path}")
                cleaned += 1

        if cleaned == 0:
            print("  No temporary files to clean")
        else:
            print(f"Cleaned {cleaned} items")

    def download_data(self) -> None:
        """Download datasets."""
        print("Downloading datasets...")
        download_script = self.project_root / "helpers" / "download_csv.py"
        if download_script.exists():
            self.run_command([self.python, str(download_script)])
        else:
            print("Download script not found!")
            sys.exit(1)

    def start_notebook(self, lab: bool = True) -> None:
        """Start Jupyter Notebook or Lab."""
        print("Starting Jupyter Lab...")
        cmd = ["jupyter", "lab", "--notebook-dir=notebooks"]

        try:
            self.run_command(cmd, check=False)
        except FileNotFoundError:
            print("Jupyter not installed. Install with: pip install jupyterlab")
            sys.exit(1)

    def show_help(self) -> None:
        """Show help message."""
        print(__doc__)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Project management script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "command",
        choices=[
            "setup",
            "install",
            "test",
            "test-cov",
            "clean",
            "data",
            "notebook",
            "help",
        ],
        help="Command to run",
    )

    args = parser.parse_args()

    manager = ProjectManager()

    try:
        if args.command == "setup":
            manager.setup()
        elif args.command == "install":
            manager.install()
        elif args.command == "test":
            manager.test(coverage=False)
        elif args.command == "test-cov":
            manager.test(coverage=True)
        elif args.command == "clean":
            manager.clean()
        elif args.command == "data":
            manager.download_data()
        elif args.command == "notebook":
            manager.start_notebook()
        elif args.command == "help":
            manager.show_help()
        else:
            parser.print_help()

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
