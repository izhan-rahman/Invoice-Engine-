# =========================================================
# Alphabit AI PDF Generation Engine - Production Dockerfile
# Base: python:3.11-slim (Debian-based, needed for WeasyPrint GTK libs)
# =========================================================

FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable stdout/stderr flushing
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies required by WeasyPrint (Cairo, Pango, GDK-Pixbuf)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    fonts-liberation \
    fonts-dejavu-core \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /app

# Install Python dependencies first (leverages Docker layer cache)
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the full project into the container
COPY . .

# Create required directories if they don't exist
RUN mkdir -p app/static/css

# Expose the application port
EXPOSE 8000

# Health check – Linux server / load balancer can use this
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')" || exit 1

# Run with Gunicorn + Uvicorn workers for production throughput
# Adjust --workers based on your server CPU count (recommended: 2 * CPU + 1)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
