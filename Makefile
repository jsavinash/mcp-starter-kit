.PHONY: help install run-stdio run-http lint format format-check typecheck test security docs docs-serve docker-build hooks-install clean

help: ## Show available targets
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z_-]+:.*## / {printf "%-18s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install all workspace apps and root development tools
	uv sync --all-packages

run-stdio: ## Run the example server over stdio
	uv run --package mcp-example-server mcp-example-server

run-http: ## Run the example server over local Streamable HTTP
	MCP_TRANSPORT=streamable-http uv run --package mcp-example-server mcp-example-server

lint: ## Run Ruff lint
	uv run ruff check .

format: ## Format Python files with Ruff
	uv run ruff format .

format-check: ## Check Ruff formatting
	uv run ruff format --check .

typecheck: ## Run MyPy
	uv run mypy apps libs main.py

test: ## Run the repository test suite
	uv run pytest -q

security: ## Audit locked Python dependencies
	uv run pip-audit

docs: ## Build the documentation site
	uv run --group docs mkdocs build --strict

docs-serve: ## Serve documentation locally
	uv run --group docs mkdocs serve

docker-build: ## Build the example MCP server image
	docker build -f apps/example-server/Dockerfile -t mcp-example-server:local .

hooks-install: ## Install standard pre-commit hooks
	uv run pre-commit install

clean: ## Remove generated caches and build artifacts
	find . -type d \( -name __pycache__ -o -name .pytest_cache -o -name .ruff_cache -o -name .mypy_cache \) -prune -exec rm -rf {} +
	rm -rf build dist site .coverage htmlcov
