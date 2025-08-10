# syntax=docker/dockerfile:1.7
FROM python:3.10-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PATH="/venv/bin:$PATH"

# System deps (adjust if you use Postgres instead of MySQL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
 && rm -rf /var/lib/apt/lists/*

# Create venv to keep site-packages tidy
RUN python -m venv /venv

WORKDIR /app

# Leverage Docker layer caching: copy requirements first
COPY requirements.txt .

# If using buildx/BuildKit, this cache mount speeds up pip installs on rebuilds
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Copy the rest of the app
COPY . .

# (Optional) create a non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Use 0.0.0.0 for in-container binding
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
