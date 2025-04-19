# Variables
SHELL := /bin/bash
PYTHON := python3
VENV_DIR := venv
COLLECTIONS_BASE := collections/ansible_collections/h33n0k
COLLECTIONS := $(wildcard $(COLLECTIONS_BASE)/*)

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

	@echo "Installing galaxy dependencies"
	@for collection in $(COLLECTIONS); do \
		req_file="$$collection/meta/requirements.yml"; \
		if [ -f "$$req_file" ]; then \
			echo "Found: $$req_file"; \
			ansible-galaxy install -r "$$req_file"; \
		else \
			echo "No requirements file in $$collection"; \
		fi \
	done

lint:
	@echo "Linting codebase"
	ansible-lint .
