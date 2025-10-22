FROM python:3.14-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.gha.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.gha.txt

# Copy project code
COPY . .

# Set PYTHONPATH
ENV PYTHONPATH=/app

# Default command
CMD ["bash"]
