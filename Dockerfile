# Dockerfile for Training Pipeline
FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY src/ src/
COPY data/ data/

# Create models directory
RUN mkdir -p models

# Run training script
CMD ["python", "src/train.py"]
