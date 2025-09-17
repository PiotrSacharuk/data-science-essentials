# data-science-essentials

Quick setup and development notes

## Install dependencies
Create and activate your virtual environment, then install dependencies from `requirements.txt`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Pre-commit hooks
Install git hooks (run once):

```bash
pre-commit install
```

Run all hooks manually:

```bash
pre-commit run --all-files
```

Notes:
- The local `pytest` hook is configured to run with `PYTHONPATH` set so tests can import `source`.
- To disable running tests in pre-commit temporarily, use `SKIP=pytest git commit -m "..."`.

## VS Code
Recommended extension: `emeraldwalk.runonsave` (auto-run commands on file save). The workspace settings include `files.autoSave` and a Run on Save command that runs `pre-commit run pytest --all-files` on `.py` saves.

## Running tests
From project root run:

```bash
PYTHONPATH=$(pwd) pytest --cov=source
```

This runs tests and shows coverage for the `source` package.
