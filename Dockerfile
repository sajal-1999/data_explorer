# Use the official Python image.
FROM python:3.9-slim

WORKDIR /code

# Install build dependencies
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project
COPY . .

# Expose the port for the app
EXPOSE 8000

# Run Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "data_explorer.wsgi:application"]
