# Variables
SHELL := /bin/bash
PYTHON := python3
VENV_DIR := venv

init:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV_DIR)

	@echo "Virtual environment created. Run the following to activate it:"
	@echo "source $(VENV_DIR)/bin/activate"
	@echo "---"

prepare:
	@echo "Installing dev dependencies"
	pip install -r requirements-dev.txt
	pre-commit install

lint:
	@echo "Linting codebase"
	ansible-lint .
