.PHONY: help install test lint format clean docker-up docker-down docker-build

help: ## Show this help message
	@echo 'Usage:'
	@echo '  make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	pip install -r requirements.txt
	cd src/web && npm install

install-dev: ## Install development dependencies
	pip install -r requirements.txt
	pip install black flake8 mypy isort pre-commit pytest pytest-cov
	cd src/web && npm install
	pre-commit install

test: ## Run tests
	pytest tests/ -v --cov=src --cov-report=term-missing

test-api: ## Run API tests
	pytest src/api/app/tests/ -v

test-web: ## Run web tests
	cd src/web && npm test

test-all: ## Run all tests
	make test-api
	make test-web

lint: ## Run linting checks
	black --check src/
	flake8 src/
	mypy src/
	cd src/web && npm run lint

format: ## Format code automatically
	black src/
	isort src/
	cd src/web && npm run format

docker-up: ## Start Docker containers
	docker-compose up -d

docker-down: ## Stop Docker containers
	docker-compose down

docker-build: ## Build Docker images
	docker-compose build

docker-logs: ## Show Docker logs
	docker-compose logs -f

migrate: ## Run database migrations
	docker-compose exec api alembic upgrade head

migrate-create: ## Create new migration
	docker-compose exec api alembic revision --autogenerate -m "$(msg)"

seed: ## Seed database with sample data
	docker-compose exec api python -m scripts.seed_database

clean: ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	rm -rf build/ dist/ *.egg-info/

coverage: ## Generate coverage report
	pytest --cov=src --cov-report=html
	@echo "Coverage report generated at htmlcov/index.html"

security-check: ## Run security checks
	bandit -r src/
	safety check

docs: ## Generate documentation
	cd docs && mkdocs build

docs-serve: ## Serve documentation locally
	cd docs && mkdocs serve

pre-commit-all: ## Run all pre-commit hooks
	pre-commit run --all-files

dev: ## Start development environment
	docker-compose up -d api web streamlit postgres redis
	@echo "Services running:"
	@echo "- API: http://localhost:8000"
	@echo "- API Docs: http://localhost:8000/docs"
	@echo "- Web App: http://localhost:3000"
	@echo "- Streamlit: http://localhost:8501"
	@echo "- PgAdmin: http://localhost:5050"

prod-build: ## Build production images
	docker-compose -f docker-compose.prod.yml build

prod-up: ## Start production environment
	docker-compose -f docker-compose.prod.yml up -d

prod-down: ## Stop production environment
	docker-compose -f docker-compose.prod.yml down
