.PHONY: install install-dev test lint format clean build docker docker-test pre-commit ci-check

# Installation
install:
	pip install -e .

install-dev:
	pip install -e .[dev]

# Testing
test:
	python -m pytest tests/ -v --cov=ctxcook --cov-report=term-missing

test-ci:
	python -m pytest tests/ -v --cov=ctxcook --cov-report=xml --cov-report=html

# Code quality
lint:
	flake8 ctxcook/ tests/
	black --check ctxcook/ tests/
	isort --check-only ctxcook/ tests/
	mypy ctxcook/

format:
	black ctxcook/ tests/
	isort ctxcook/ tests/

# Pre-commit
pre-commit:
	pre-commit install
	pre-commit run --all-files

# CI checks
ci-check: lint test-ci

# Building
clean:
	rm -rf __pycache__/
	rm -rf *.egg-info/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/

build: clean
	python -m build

# Docker
docker-build:
	docker build -f Dockerfile.ci -t ctxos/cookbook:latest .

docker-test:
	docker run --rm -v $(pwd)/cookbooks:/app/cookbooks ctxos/cookbook:latest ctxcook info cookbooks/llm_finetune.yaml

docker-run:
	docker run --rm -v $(pwd)/cookbooks:/app/cookbooks -v $(pwd)/output:/app/output ctxos/cookbook:latest ctxcook build cookbooks/semantic_search.yaml --output output/semantic.ipynb

# Examples
example:
	ctxcook build cookbooks/llm_finetune.yaml --output notebooks/finetune.ipynb

example-all:
	ctxcook build cookbooks/multimodal_vision.yaml --output notebooks/multimodal_vision.ipynb --environment colab
	ctxcook build cookbooks/semantic_search.yaml --output notebooks/semantic_search.ipynb --requirements semantic_requirements.txt
	ctxcook build cookbooks/llm_inference_server.yaml --output notebooks/llm_inference_server.ipynb --dockerfile Dockerfile.example --hf-deploy hf_deploy.example.yaml

# Validation
validate-cookbooks:
	@python scripts/validate_cookbooks.py

# Development helpers
dev-setup: install-dev pre-commit
	@echo "Development environment setup complete!"
	@echo "Run 'make test' to run tests"
	@echo "Run 'make lint' to check code quality"

# Release
release-patch:
	@bump2version patch
	@echo "Patch version bumped. Run 'git push --tags' to release."

release-minor:
	@bump2version minor
	@echo "Minor version bumped. Run 'git push --tags' to release."

release-major:
	@bump2version major
	@echo "Major version bumped. Run 'git push --tags' to release."
