# mcp-starter-kit

# 🏗️ Python Monorepo Starter Kit

A production-grade Python monorepo starter kit featuring **Django REST API**, **Flask REST API**, and **Streamlit Frontend** templates — all managed with `uv` workspace for unified dependency management.

## 📋 Current State

```
python-starter-kit/
│
├── apps/                          # Application projects (planned)
│   ├── django-api/                # Django REST API - Not yet created
│   ├── flask-api/                 # Flask REST API - Not yet created
│   ├── frontend/                  # Streamlit Frontend - Not yet created
│   └── web/                       # React web frontend (boilerplate)
│
├── libs/                          # Shared libraries
│   └── shared/                    # Common DTOs, contracts, utilities (Pydantic)
│
├── educational-resources/         # Learning materials
│   └── python-programming/        # Python programming resources
│
├── config/                        # Configuration
│   └── dependencies.toml          # Centralized dependency version catalog
│
├── docs/                          # MkDocs documentation site
│
├── tests/                         # Root-level tests
│
├── .github/workflows/             # CI/CD pipelines (GitHub Actions)
├── .githooks/                     # Custom git hooks (pre-commit, commit-msg, pre-push)
│
├── pyproject.toml                 # Root workspace config
├── docker-compose.yml             # Service orchestration (Redis, app templates)
├── Makefile                       # Development automation
├── main.py                        # Root entry point
└── .pre-commit-config.yaml        # Pre-commit framework hooks
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (package manager)
- Docker & Docker Compose (optional)

### Install Dependencies
```bash
# Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install
git clone <repo-url>
cd python-starter-kit
make install
```

### Install Git Hooks
```bash
# Custom bash hooks (recommended - branch protection, secret scanning, quality checks)
bash scripts/install-hooks.sh

# Pre-commit framework hooks
uv run pre-commit install
```

### Run Root CLI
```bash
uv run python main.py
# → Hello from python-starter-kit!
```

## 📖 Features

### Current Implementation

| Feature | Status | Details |
|---------|--------|---------|
| **uv Workspace** | ✅ Complete | Unified dependency management with single lockfile |
| **Shared Library** | ✅ Complete | `libs/shared` with Pydantic DTOs, contracts, utilities |
| **Custom Git Hooks** | ✅ Complete | 9 pre-commit checks, commit message validation, 6 pre-push checks |
| **Secret Scanning** | ✅ Complete | High-confidence pattern detection for credentials & API keys |
| **Centralized Dep Catalog** | ✅ Complete | `config/dependencies.toml` - single source of truth for versions |
| **CI/CD Pipeline** | ✅ Complete | GitHub Actions with lint, test matrix, security, docker, package jobs |
| **Docker Orchestration** | ✅ Complete | Docker Compose with Redis, templated app services |
| **MkDocs Documentation** | ✅ Complete | Material theme, API docs via mkdocstrings |
| **Code Quality** | ✅ Complete | Ruff lint, Ruff format, MyPy strict mode, Pytest with coverage |
| **React Web App** | ✅ Boilerplate | `apps/web` - Vite + React + TypeScript + Vitest |

### Planned Applications

| App | Framework | Port | Description |
|-----|-----------|------|-------------|
| `apps/django-api` | Django 5.0 + DRF | 8000 | JWT auth, user management, Swagger docs, Celery tasks |
| `apps/flask-api` | Flask 3.0 + SQLAlchemy | 5000 | Blueprint pattern, Marshmallow validation, Celery tasks |
| `apps/frontend` | Streamlit 1.35+ | 8501 | Dashboard UI, auth forms, Plotly charts, httpx client |

### App Scaffolding (when apps are created)

```bash
# Each app will have its own:
├── src/                    # Application source code
├── tests/                  # Pytest test suite
├── Dockerfile              # Multi-stage Docker build
├── pyproject.toml          # App-specific dependencies
└── .env                    # Environment configuration
```

## 📦 Dependency Management

### Centralized Version Catalog

All dependency versions are managed centrally in `config/dependencies.toml` — the single source of truth for the entire monorepo. This file catalogs every dependency organized by ecosystem (Django, Flask, FastAPI, testing, linting, etc.).

### How to Manage Dependencies

```bash
# View the dependency catalog
make dep-catalog

# List all workspace dependencies
make dep-list

# Check for outdated dependencies
make dep-outdated

# Add a dependency
uv add <package>

# Upgrade all dependencies
make dep-upgrade-all

# Verify no dependency conflicts
make dep-verify

# Audit for vulnerabilities
make dep-audit

# Check dependency licenses
make dep-licenses
```

## 🛠️ Development Workflow

### Code Quality
```bash
make lint          # Ruff lint check
make format        # Ruff auto-format
make format-check  # Check formatting without changes
make typecheck     # MyPy type checking
make test          # Run all tests
make test-cov      # Tests with coverage report
make quality-check # All quality checks combined
make quality-fix   # Auto-fix all quality issues
make test-all      # Full suite: test + quality
```

### Clean Build
```bash
make clean        # Clean Python cache artifacts
make deep-clean   # Remove all build/cache artifacts (venv, node_modules, etc.)
make full-build   # Full pipeline: install + test + quality
```

### Docker Commands
```bash
make docker-build          # Build all images
make docker-up             # Start services
make docker-down           # Stop all services
make docker-logs           # View all logs
```

## 🔧 Configuration

### Environment Variables

Copy the example env file and customize:

```bash
cp .env.example .env
```

See `.env.example` for all available configuration options including:
- Django, Flask, and Streamlit settings
- Database connection strings
- Redis configuration
- JWT secrets
- Sentry DSN
- AWS credentials

### Python Version

```bash
cat .python-version
# → 3.12
```

## 🔐 Security

### Multi-Layer Protection

1. **Pre-commit Hook**: Secret scanning, credential detection, private key checks
2. **Pre-push Hook**: Dependency vulnerability audit via `pip-audit`
3. **CI/CD Pipeline**: Automated security scanning on every push/PR

### Supported Secret Patterns
- AWS Access Keys (`AKIA...`)
- Private Keys (`-----BEGIN PRIVATE KEY-----`)
- GitHub Tokens (`ghp_...`, `gho_...`, `github_pat_...`)
- OpenAI API Keys (`sk-...`)
- Slack Tokens (`xox[baprs]-...`)
- Stripe Keys (`pk_live_...`, `sk_live_...`)

## 📊 Quality Gates

| Layer | Check | Timing |
|-------|-------|--------|
| **Pre-Commit** | Branch protection, file validation, commit message format, secret scanning, Ruff format, Ruff lint, MyPy, quick tests | On `git commit` |
| **Pre-Push** | Branch protection, full test suite, full quality check, commit history, dependency audit | On `git push` |
| **CI/CD** | Lint, test matrix (3.10/3.11/3.12), security audit, Docker build, package build | GitHub Actions |

## 🤝 Contributing

1. Install hooks: `bash scripts/install-hooks.sh`
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Make changes and run quality checks: `make test-all`
4. Commit using conventional commits: `git commit -m "feat(scope): description"`
5. Push and create a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📚 Documentation

- [Architecture Overview](ARCHITECTURE.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Monorepo Improvements](MONOREPO_IMPROVEMENTS.md)

## 📄 License

MIT License - see LICENSE file for details.
