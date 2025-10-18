.PHONY: venv install run-dev run-pro test test-ci format format-check lint lint-fix \
        container-lint refactor clean all free-port docker-build docker-run-dev docker-run-pro

venv:
	@test -d .venv || uv venv

install: venv
	@if [ -f pyproject.toml ]; then \
		echo "Using pyproject.toml with uv sync --dev"; \
		uv sync --dev; \
	else \
		echo "No pyproject.toml found. Installing from requirements.txt (if present)"; \
		if [ -f requirements.txt ]; then uv pip install -r requirements.txt; fi; \
		echo "Adding dev dependencies (pytest, pytest-cov, ruff)"; \
		uv pip install -U pytest pytest-cov ruff; \
	fi

run-dev:
	@echo "Starting dev server on http://127.0.0.1:8000"
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

run-pro:
	@echo "Starting prod server on http://127.0.0.1:8000"
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000

test:
	@echo "Running tests (verbose + coverage)"
	uv run -m pytest -vv \
		--cov=app --cov-branch --cov-report=term-missing \
		--cov-fail-under=90 tests/

test-ci:
	@echo "Running tests (CI mode)"
	uv run -m pytest -q --maxfail=1 --disable-warnings \
		--cov=app --cov-branch --cov-report=term-missing \
		--cov-fail-under=90 tests/

format:
	@echo "Formatting with Ruff"
	uv run ruff format app tests

format-check:
	@echo "Checking format with Ruff"
	uv run ruff format --check app tests

lint:
	@echo "Linting with Ruff"
	uv run ruff check app tests

lint-fix:
	@echo "Linting & fixing with Ruff"
	uv run ruff check app tests --fix

container-lint:
	@echo "Linting Dockerfile with hadolint"
	docker run --rm -i hadolint/hadolint < Dockerfile

refactor: format lint

clean:
	@echo "Cleaning build/test artifacts"
	rm -rf .venv .pytest_cache .ruff_cache .coverage htmlcov \
		build dist *.egg-info **/*.egg-info

free-port:
	@echo "Attempting to free port 8000..."
	@if command -v lsof > /dev/null; then \
		PID=$$(sudo lsof -t -i :8000); \
		if [ -n "$$PID" ]; then \
			echo "Found process(es) with PID(s): $$PID on port 8000. Killing them..."; \
			echo "$$PID" | sudo xargs kill -9; \
			echo "Port 8000 should be free now."; \
		else \
			echo "Port 8000 is not currently in use by any identifiable process."; \
		fi; \
	else \
		echo "lsof command not found. Cannot automatically kill the process. Try 'sudo kill -9 $$(sudo lsof -t -i :8000)' manually."; \
	fi

all: install format lint test

# --- Docker Commands ---
docker-build:
	@echo "Building Docker image..."
	docker build -t open-weather-map .

docker-run-pro:
	@echo "Running Docker container in production mode..."
	docker run -p 8000:8000 --rm --name open-weather-map-pro open-weather-map

docker-run-dev:
	@echo "Running Docker container in development mode with hot-reload..."
	docker run -p 8000:8000 --rm --name open-weather-map-dev -v ./app:/app/app -e open-weather-map uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
