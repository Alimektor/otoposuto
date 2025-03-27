# Variables
PACKAGE_NAME = otoposuto


.PHONY: all install clean venv precommit editable dev update help
all: install update clean ## Build the package and clean the Git repository (Default target)

build: ## Build the package
	$(info "Building Python package...")
	poetry build
	$(info "Package built successfully.")

install: build ## Install the package in the system
	pip3 install dist/*.whl

venv: ## Install the package in the virtual environment
	$(info "Creating Poetry virtual environment...")
	poetry install
	poetry config virtualenvs.create true --local
	poetry config virtualenvs.in-project true --local
	$(info "Created Poetry virtual environment successfully.")

clean: ## Clean the Git repository
	$(info "Cleaning up the Git repository...")
	git gc
	git prune
	git clean -Xfd
	$(info "Git repository cleaned.")

precommit: ## Install precommit hooks for the virtual environment
	$(info "Adding precommit hooks...")
	poetry run pre-commit install
	$(info "Running precommit hooks...")
	poetry run pre-commit run
	$(info "Precommit hooks installed successfully.")

dev: venv precommit ## Development the package
	$(info "Installing development dependencies...")
	poetry install --with dev
	$(info "Development dependencies installed successfully.")

update: ## Update the package requirements
	$(info "Updating package requirements...")
	poetry run pip-compile --output-file=requirements.txt pyproject.toml
	$(info "Package requirements updated successfully.")

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[1;32m%-15s \033[1;33m%s\033[0m\n", $$1, $$2}'
