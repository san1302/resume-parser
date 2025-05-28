FROM python:3.9-slim

WORKDIR /app

# Install system dependencies needed for document processing
RUN apt-get update && apt-get install -y \
    antiword \
    unrtf \
    poppler-utils \
    tesseract-ocr \
    libjpeg-dev \
    swig \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install spaCy model
RUN python -m spacy download en_core_web_sm

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"] 