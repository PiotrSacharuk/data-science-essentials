# Data Science Essentials

A professional Python project template for data science workflows with best practices, testing, and automated setup.

## Project Structure

This project has been restructured to better support FastAPI application with modular data processing.

```
/
├── app/                          # FastAPI application
│   ├── __init__.py
│   ├── server.py                 # FastAPI app initialization
│   ├── api/                      # API package
│   │   └── __init__.py
│   ├── models/                   # Pydantic request/response models
│   │   ├── __init__.py
│   │   └── pandas.py             # Pandas data models
│   └── routes/                   # API route handlers
│       ├── __init__.py
│       └── pandas.py             # Pandas data endpoints
│
├── src/                          # Source code library
│   ├── __init__.py
│   ├── data/                     # Data modules
│   │   ├── __init__.py
│   │   ├── sources/              # Data sources (CSV loading, etc.)
│   │   │   ├── __init__.py
│   │   │   └── pandas_source.py  # PandasSource implementation
│   │   └── processors/           # Data processors (placeholder)
│   │       └── __init__.py
│   └── utils/                    # Utility modules
│       ├── __init__.py
│       ├── cache/                # Cache management utilities
│       │   ├── __init__.py
│       │   └── cache_manager.py  # File caching with concurrent protection
│       └── network/              # Network utilities
│           ├── __init__.py
│           └── url_utils.py      # URL validation and MD5 hash generation
│
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── conftest.py               # Pytest configuration and fixtures
│   ├── app/                      # Tests for FastAPI application
│   │   ├── __init__.py
│   │   ├── test_server.py        # App initialization and routing tests
│   │   ├── models/               # Tests for app models
│   │   │   ├── __init__.py
│   │   │   └── test_pandas.py    # Pydantic model validation tests
│   │   └── routes/               # Tests for app routes
│   │       ├── __init__.py
│   │       └── test_pandas.py    # API endpoint tests
│   ├── data/                     # Tests for data modules
│   │   ├── __init__.py
│   │   └── sources/
│   │       ├── __init__.py
│   │       └── test_pandas_source.py
│   └── utils/                    # Tests for utility modules
│       ├── __init__.py
│       ├── cache/
│       │   ├── __init__.py
│       │   └── test_cache_manager.py
│       └── network/
│           ├── __init__.py
│           └── test_url_utils.py
│
├── data/                         # Data directory
│   ├── raw/                      # Raw data (iris.csv)
│   └── cache/                    # Cached downloaded files
│
├── helpers/                      # Helper utilities
│   └── download_csv.py           # Iris dataset download script
│
├── notebooks/                    # Jupyter Notebooks
│   ├── README.md
│   └── exploratory/
│       ├── 01_iris_data_exploration.ipynb
│       └── 02_url_data_loading_test.ipynb
│
├── .github/                      # GitHub configuration
│   ├── scripts/
│   │   └── post_test_report.py   # Test report post-processing script
│   └── workflows/                # GitHub Actions workflows
│       ├── pre-commit.yml        # Code quality checks (black, isort, flake8, mypy, bandit, pytest)
│       ├── test-report.yml       # Test reporting on PRs
│       └── test-notebooks.yml    # Notebook execution tests
│
├── setup.py                      # Project setup and initialization script
├── make.py                       # Development task runner (setup, install, run, test, etc.)
├── config.yaml                   # Project configuration (directories, datasets)
├── .env.example                  # Environment variables template
├── .pre-commit-config.yaml       # Pre-commit hooks configuration
├── .coveragerc                   # Coverage report configuration
├── .gitignore                    # Git ignore rules
├── pytest.ini                    # Pytest configuration
├── pyproject.toml                # Python project metadata
├── requirements.txt              # Project dependencies (full list)
├── requirements.gha.txt          # Optimized dependencies for GitHub Actions
├── jupyter-run.sh                # Jupyter notebook launcher script
├── notebook-requirements.txt     # Jupyter-specific dependencies
└── README.md                     # This file
```

## Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/PiotrSacharuk/data-science-essentials.git
cd data-science-essentials

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Run automated setup
python setup.py
```

This will:
- Create complete project directory structure
- Download required datasets (configured in config.yaml)
- Install Python dependencies
- Set up development environment

### 2. Verify Installation
```bash
# Run tests
python make.py test

# Start Jupyter Lab
python make.py notebook
```

## Data Processing with PandasSource

The `PandasSource` class provides a unified interface for working with CSV data from both local files and remote URLs, with automatic caching and concurrent access protection.

### Features

- **Unified Interface**: Same API for local files and remote URLs
- **Automatic Caching**: Downloads are cached locally for faster subsequent access
- **Concurrent Protection**: Safe to use in multi-process environments
- **Flexible Configuration**: Support for various CSV formats and parameters

### Usage Examples

#### Local Files
```python
from src.data.sources.pandas_source import PandasSource

# Load local CSV file
source = PandasSource('data/raw/iris.csv', header=True)
print(f"Data shape: {source.df.shape}")
print(source.head())
```

#### Remote URLs
```python
# Load data from URL (automatically cached)
iris_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
column_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']

source = PandasSource(iris_url, names=column_names)
print(f"Loaded from: {source.original_source}")
print(f"Cached at: {source.file_path}")
print(source.describe())
```

#### Advanced Configuration
```python
# Custom separator and cache directory
source = PandasSource(
    'https://example.com/data.csv',
    separator=';',
    decimal=',',
    header=True,
    cache_dir='custom_cache',
    timeout=60
)

# Get metadata about the data source
metadata = source.metadata
print(f"Source type: {metadata['source_type']}")
print(f"Shape: {metadata['shape']}")
```

#### Cache Management
```python
# Refresh cached data (re-download from URL)
source.refresh_cache()

# Check cache status
if source.is_url:
    print(f"Cache directory: {source.cache_dir}")
    print(f"Is cached: {source.metadata['is_cached']}")
```

### Architecture

The PandasSource implementation is built on modular utilities:

- **`src.utils.network.url_utils`**: URL validation and cache path generation
- **`src.utils.cache.cache_manager`**: Robust file caching with concurrent access protection
- **Atomic Operations**: Downloads use temporary files and atomic moves
- **File Locking**: Prevents concurrent download conflicts

## Development Commands

We use `make.py` as a task runner (Python equivalent of Makefile):

```bash
# Project setup
python make.py setup          # Complete project setup
python make.py install        # Install dependencies

# Development
python make.py run            # Start FastAPI development server
python make.py test           # Run tests
python make.py test-cov       # Run tests with coverage
python make.py clean          # Clean temporary files

# Jupyter
python make.py notebook       # Start Jupyter Lab
python make.py data           # Download datasets

# Help
python make.py help           # Show help message
```

## Testing

```bash
# Run all tests
python make.py test

# Run with coverage report
python make.py test-cov

# Run specific test file
pytest tests/data/sources/test_pandas_source.py -v

# Run app tests only
pytest tests/app/ -v

# Run with coverage for specific module
pytest tests/ --cov=app --cov-report=term-missing
```

### Test Coverage

The project has comprehensive test coverage with well-organized test structure that mirrors the source code organization:

- **`tests/app/`** - FastAPI application tests (42 tests)
  - `test_server.py` - App initialization and route mounting (7 tests)
  - `models/test_pandas.py` - Pydantic request model validation (20 tests)
    - Parametrized tests for efficient validation coverage
    - Shared `BASE_URL` constant (DRY principle)
  - `routes/test_pandas.py` - Pandas API endpoints testing (15 tests)
    - Reusable CSV creation helper (`create_csv_file`)
    - Common response assertion helper (`assert_success_response`)
    - Parametrized endpoint tests for head/tail

- **`tests/src/`** - Source library tests (64 tests)
  - `tests/data/sources/` - PandasSource implementation tests
  - `tests/utils/cache/` - Cache management and concurrent access tests
  - `tests/utils/network/` - URL validation and caching utilities tests

**Overall Coverage: 100%** on all modules (`app/` and `src/`)

#### Test Organization Principles

The test suite follows best practices:
- **DRY (Don't Repeat Yourself)**: Shared fixtures, constants, and helper functions
- **KISS (Keep It Simple, Stupid)**: Parametrized tests reduce code duplication
- **Mirrored Structure**: `tests/` directory mirrors `src/` and `app/` organization
  - `tests/data/sources/` - PandasSource implementation tests
  - `tests/utils/cache/` - Cache management and concurrent access tests
  - `tests/utils/network/` - URL validation and caching utilities tests

**Overall Coverage: 100%** on all modules (`app/` and `src/`)


## Using the Data Sources API

```python
from src.data.sources import PandasSource

# Load data from CSV
data_source = PandasSource(
    file_path="data/raw/iris.csv",
    separator=",",
    header=False,
    names=["sepal_length", "sepal_width", "petal_length", "petal_width", "target"]
)

# Explore data
print(data_source.head())
print(data_source.describe())
```

## Jupyter Notebooks

```bash
# Start Jupyter Lab
python make.py notebook
```

See [`notebooks/README.md`](notebooks/README.md) for detailed guidelines and best practices.

## Project Configuration

The project uses `config.yaml` for configuration. This allows you to easily:

- Add new directories to the project structure
- Add new datasets to download automatically
- Configure default parameters

Example configuration:

```yaml
# Project Configuration

# Directories to create (relative to project root)
directories:
  - data/raw
  - data/processed
  - notebooks/exploratory
  # Add more directories as needed

# Datasets to download
datasets:
  - name: iris
    url: https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data
    filename: iris.csv
    destination: data/raw
  # Add more datasets by following the same format
```

To add a new dataset, simply edit `config.yaml` and run `python setup.py` again.

## Pre-commit Hooks

Install git hooks for code quality:

```bash
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

## Features

- **Professional Structure** - Industry-standard project organization
- **Automated Setup** - One command to set up everything
- **Data Management** - Separate raw/processed data with automated downloads
- **Testing Framework** - Comprehensive tests with coverage reporting
- **Jupyter Integration** - Organized notebooks with guidelines
- **Documentation** - Comprehensive docs and examples
- **Configuration-Driven** - External YAML configuration file for easy customization

## Future Development

This structure is designed to support:
- FastAPI integration for data processing via API
- Modular data processing pipelines
- Clear separation of data sources and processors
- **Team Collaboration** - Clear conventions and documentation
- **Extensible Design** - Easy to add new components
- **Maintainable Code** - Clean separation of concerns

## Resources

- [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/)
- [Jupyter Notebook Best Practices](notebooks/README.md)
- [Python Package Structure Guide](https://packaging.python.org/)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`python make.py test`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Happy Data Science!**
