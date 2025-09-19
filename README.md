# Data Science Essentials

A professional Python project template for data science workflows with best practices, testing, and automated setup.

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

## Project Structure

```
data-science-essentials/
├── notebooks/             # Jupyter notebooks organized by purpose
│   ├── exploratory/       # Data exploration and analysis
│   └── reports/           # Final reports for stakeholders (if needed)
├── data/                  # Data storage (not in repo)
│   ├── raw/               # Original, immutable datasets
│   └── processed/         # Cleaned, transformed data
├── source/                # Source code for production
│   └── data_readers/      # Data loading utilities
├── tests/                 # Unit tests
├── reports/               # Generated reports and figures
├── helpers/               # Utility scripts
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
pytest tests/data_readers/test_pandas_data_reader.py -v
```

## Using the Data Readers

```python
from source.data_readers.pandas_data_reader import PandasDataReader

# Load data with proper error handling
import os

file_path = 'data/raw/iris.csv'
if os.path.exists(file_path):
    # Using PandasDataReader
    reader = PandasDataReader(
        file_path=file_path,
        separator=',',
        header=0
    )
    df = reader.read_csv_file()
    print(df.head())
else:
    print(f"Warning: File {file_path} does not exist.")
```

## Jupyter Notebooks

```bash
# Start Jupyter Lab
python make.py notebook
```

See [`notebooks/README.md`](notebooks/README.md) for detailed guidelines and best practices.

## Pre-commit Hooks

Install git hooks for code quality:

```bash
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

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

## Features

- **Professional Structure** - Industry-standard project organization
- **Automated Setup** - One command to set up everything
- **Data Management** - Separate raw/processed data with automated downloads
- **Testing Framework** - Comprehensive tests with coverage reporting
- **Jupyter Integration** - Organized notebooks with guidelines
- **Documentation** - Comprehensive docs and examples
- **Configuration-Driven** - External YAML configuration file for easy customization

## Future-Ready

This structure is designed to scale with your project:

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
