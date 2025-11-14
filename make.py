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
    run-fastapi - Start FastAPI development server from fastapi cmd
    run-python  - Start FastAPI development server from python cmd
    test        - Run tests
    test-cov    - Run tests with coverage
    clean       - Clean temporary files
    data        - Download datasets
    notebook    - Start Jupyter Lab
    git-hooks   - Set up pre-commit git hooks
    fix-hooks   - Fix code formatting issues
    help        - Show this help message

Examples:
    python make.py setup
    python make.py run-fastapi
    python make.py test-cov
    python make.py git-hooks
    python make.py fix-hooks
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
        """Install dependencies using Poetry."""
        print("Installing dependencies with Poetry...")
        try:
            self.run_command(["poetry", "install"])
        except FileNotFoundError:
            print("Poetry not found! Install it with:")
            print("curl -sSL https://install.python-poetry.org | python -")
            sys.exit(1)

    def test(self, coverage: bool = False) -> None:
        """Run tests."""
        cmd = [self.python, "-m", "pytest", "tests/"]

        if coverage:
            print("Running tests with coverage...")
            cmd.extend(
                [
                    "--cov=src",
                    "--cov=app",
                    "--cov-report=term-missing",
                    "--cov-report=html",
                ]
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
            "data/cache",
            "notebooks/**/data/cache",
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

    def setup_git_hooks(self) -> None:
        """Set up git hooks using pre-commit."""
        print("Setting up git hooks with pre-commit...")

        # Check if pre-commit config exists
        config_file = self.project_root / ".pre-commit-config.yaml"
        if not config_file.exists():
            print("ERROR: .pre-commit-config.yaml not found!")
            print("Please create .pre-commit-config.yaml first")
            sys.exit(1)

        try:
            # Install pre-commit hooks
            print("Installing pre-commit hooks...")
            self.run_command(["poetry", "run", "pre-commit", "install"])

            # Install commit-msg hook for conventional commits
            print("Installing commit-msg hook...")
            self.run_command(
                ["poetry", "run", "pre-commit", "install", "--hook-type", "commit-msg"]
            )

            # Run pre-commit on all files to test setup
            print("Testing hooks on all files...")
            try:
                self.run_command(
                    ["poetry", "run", "pre-commit", "run", "--all-files"], check=False
                )
                print("Git hooks installed successfully!")
                print("\nHooks that will run before each commit:")
                self.show_hook_info()
            except subprocess.CalledProcessError:
                print("WARNING: Some hooks failed on existing files.")
                print("Run 'python make.py fix-hooks' to fix formatting issues.")

        except FileNotFoundError:
            print("ERROR: pre-commit not found! Install it first:")
            print("poetry add --group dev pre-commit")
            sys.exit(1)

    def fix_hooks(self) -> None:
        """Fix code formatting and style issues."""
        print("Fixing code formatting and style issues...")

        try:
            # Run only fixable hooks
            print("Running black formatter...")
            self.run_command(["poetry", "run", "black", "."], check=False)

            print("Running isort import sorter...")
            self.run_command(["poetry", "run", "isort", "."], check=False)

            print("Code formatting fixed!")
            print("You can now commit your changes.")

        except FileNotFoundError as e:
            print(f"ERROR: Tool not found: {e}")
            print("Make sure you have installed dev dependencies:")
            print("poetry install")

    def show_hook_info(self) -> None:
        """Show information about configured hooks."""
        config_file = self.project_root / ".pre-commit-config.yaml"
        if config_file.exists():
            print("Configured pre-commit hooks:")
            print("  - trailing-whitespace - removes trailing spaces")
            print("  - end-of-file-fixer - ensures files end with newline")
            print("  - check-yaml - validates YAML syntax")
            print("  - check-added-large-files - prevents large files")
            print("  - black - code formatting")
            print("  - isort - import sorting")
            print("  - flake8 - code linting")
            print("  - mypy - type checking")
            print("  - bandit - security linting")
            print("  - pytest-cov - runs tests with coverage")
        else:
            print("No pre-commit configuration found.")

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
            print(
                "Jupyter not installed."
                "Install project dependencies with: poetry install --with notebooks"
            )
            sys.exit(1)

    def run_server_cmd(self, cmd: list[str]) -> None:
        """Start FastAPI development server."""
        print("Starting FastAPI development server...")

        try:
            self.run_command(cmd, check=False)
        except FileNotFoundError:
            print(
                "FastAPI not installed."
                "Install project dependencies with: poetry install"
            )
            sys.exit(1)

    def run_from_fastapi(self) -> None:
        """Start FastAPI development server using fastapi cmd."""
        self.run_server_cmd(["fastapi", "dev", "app/server.py"])

    def run_from_python(self) -> None:
        """Start FastAPI development server using python cmd."""
        self.run_server_cmd(["python", "app/server.py"])

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
            "run-fastapi",
            "run-python",
            "test",
            "test-cov",
            "clean",
            "data",
            "notebook",
            "git-hooks",
            "fix-hooks",
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
        elif args.command == "run-fastapi":
            manager.run_from_fastapi()
        elif args.command == "run-python":
            manager.run_from_python()
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
        elif args.command == "git-hooks":
            manager.setup_git_hooks()
        elif args.command == "fix-hooks":
            manager.fix_hooks()
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
