# Data Science Essentials

A professional Python project template for data science workflows with best practices, testing, and automated setup.

## Project Structure

This project has been restructured to better support future development with FastAPI and modular data processing.

```
/
├── app/                          # FastAPI application (future)
│   ├── __init__.py
│   └── api/                      # API endpoints
│       └── __init__.py
│
├── src/                          # Source code library
│   ├── __init__.py
│   ├── data/                     # Data modules
│   │   ├── __init__.py
│   │   ├── sources/              # Data sources (e.g., CSV loading)
│   │   │   ├── __init__.py
│   │   │   └── pandas_source.py  # PandasSource implementation
│   │   └── processors/           # Data processors (future)
│   │       └── __init__.py
│   └── utils/                    # Utility tools
│       └── __init__.py
│
├── tests/                        # Tests
│   ├── __init__.py
│   └── data/                     # Tests for data modules
│       ├── __init__.py
│       └── sources/              # Tests for data sources
│           ├── __init__.py
│           └── test_pandas_source.py
│
├── data/                         # Data directory
│   ├── raw/                      # Raw data
│   └── processed/                # Processed data
│
├── notebooks/                    # Jupyter Notebooks
│   └── exploratory/
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

## Development Commands

We use `make.py` as a task runner (Python equivalent of Makefile):

```bash
# Project setup
python make.py setup          # Complete project setup
python make.py install        # Install dependencies

# Development
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
```

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
