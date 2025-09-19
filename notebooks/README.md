# Notebooks Directory

This directory contains Jupyter notebooks organized by purpose and development stage.

## Directory Structure

```
notebooks/
├── exploratory/          # Exploratory Data Analysis (EDA)
└── reports/              # Final notebooks for stakeholders (if needed)
```

## Notebook Organization

### `exploratory/`
Notebooks for initial data exploration, visualization, and hypothesis generation.

**Naming convention:** `[number]_[descriptive_name].ipynb`

Example:
- `01_iris_data_exploration.ipynb` - Initial exploration of Iris dataset

### `reports/`
Polished notebooks ready for stakeholders, with clear narratives and conclusions.

**Naming convention:** `[project]_[type]_[date].ipynb`

Example:
- `iris_analysis_report_2025-09-19.ipynb` - Final analysis report

## Best Practices

### **Notebook Structure**
1. **Header** - Title, author, purpose, date
2. **Setup** - Imports, configuration, constants
3. **Data Loading** - Load and validate data
4. **Analysis** - Main analysis with clear sections
5. **Conclusions** - Key findings and next steps

### **Code Standards**
- Use meaningful variable names
- Add markdown cells to explain each section
- Include docstrings for custom functions
- Use relative paths from notebook location
- Save figures to `../../reports/figures/`

### **Visualization Guidelines**
- Consistent styling with seaborn or plotly
- Clear titles, labels, and legends
- Save plots as high-resolution PNG/PDF
- Use colorblind-friendly palettes

### **File Management**
- Clear, descriptive filenames
- Version notebooks when making major changes
- Clean up cell outputs before committing
- Use templates for new notebooks

## Getting Started

### 1. Create a New Notebook
```bash
# Create a new notebook in the exploratory directory
touch notebooks/exploratory/01_new_analysis.ipynb
```

### 2. Set Up Environment
```python
# Standard setup
import os
import sys
import pandas as pd
import numpy as np

# Configuration
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)

# Set random seed for reproducibility
np.random.seed(42)
```

### 3. Load Data
```python
# Use pandas directly with proper error handling
import os

file_path = '../../data/raw/your_dataset.csv'
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    print(f"Dataset shape: {df.shape}")
else:
    print(f"Warning: File {file_path} does not exist.")
```

## Tips for Effective Notebooks

### **Do:**
- Start with a clear purpose statement
- Use markdown cells liberally
- Keep cells focused and small
- Restart and run all cells before sharing
- Include data quality checks
- Document assumptions and decisions

### **Don't:**
- Create notebooks longer than 100 cells
- Leave debugging code in final versions
- Hardcode file paths
- Ignore data quality issues
- Skip documentation
- Commit notebooks with large outputs

## Collaboration Guidelines

### **Before Committing:**
1. Clear all cell outputs (unless necessary)
2. Run "Restart & Run All" to verify
3. Check for hardcoded paths or credentials
4. Add meaningful commit messages

### **Code Review:**
- Focus on analysis logic and conclusions
- Check for reproducibility
- Verify data handling practices
- Review visualization choices

## Resources

### **Documentation:**
- [Jupyter Documentation](https://jupyter.readthedocs.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)
- [Seaborn Tutorial](https://seaborn.pydata.org/tutorial.html)

### **Best Practices:**
- [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/)
- [Netflix Notebook Guidelines](https://netflixtechblog.com/notebook-innovation-591ee3221233)

---

**Need help?** Check the template notebook or ask the team!
