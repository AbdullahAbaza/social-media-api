FROM python:3.13-slim

# Set environment variables
ENV USER=fastapi \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/usr/local
    

# Install system dependencies and create user
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -s /bin/bash $USER

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
ENV APP_DIR=/home/$USER/src
WORKDIR $APP_DIR

# Copy dependency files
COPY ./pyproject.toml ./uv.lock ./alembic.ini ./prestart.sh $APP_DIR/

# Install Python dependencies using uv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

# Copy application code
COPY ./alembic $APP_DIR/alembic
COPY ./app $APP_DIR/app

# Sync the project again to ensure everything is up-to-date
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen 

# Set Python path
ENV PYTHONPATH=$APP_DIR

# Change ownership of the application directory
RUN chown -R "$USER:$USER" $APP_DIR

# Switch to the non-root user
USER $USER

# Run the application
CMD ["uvicorn", "--workers", "4", "app.main:app", "--port", "8000", "--host", "0.0.0.0"]