# -------------------------------
# Base image
# -------------------------------
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS build

# -------------------------------
# Set working directory
# -------------------------------
WORKDIR /app

# -------------------------------
# Copy project files
# -------------------------------
COPY pyproject.toml uv.lock ./
COPY app ./app
COPY README.md ./

# -------------------------------
# Install dependencies
# -------------------------------
RUN uv sync --no-dev --frozen

# -------------------------------
# Runtime stage
# -------------------------------
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

COPY --from=build /app /app

# Set environment to production
ENV ENVIRONMENT=production

EXPOSE 8000

# -------------------------------
# Command to run FastAPI app
# -------------------------------
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
