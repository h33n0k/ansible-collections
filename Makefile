# Variables
SHELL := /bin/bash
MAKEFLAGS += --no-print-directory
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

test: ## Run molecule test on all or specific role
	@echo -e "\n" > /dev/tty 2>&1
	for collection in $(COLLECTIONS); do \
		roles_dir="$$collection/roles"; \
		if [ -d "$$roles_dir" ]; then \
			for role in $$roles_dir/*; do \
				if [ -n "$(ROLE)" ]; then \
					[ "$$(basename $$collection)/$$(basename $$role)" != "$(ROLE)" ] && continue; \
				fi; \
				if [ -d "$$role" ]; then \
					config="$$role/molecule/default/molecule.yml"; \
					if [ -f "$$config" ]; then \
						if [ "$(STAGED_ONLY)" = "true" ]; then \
							scope=$$(git diff --cached --name-only | grep "^$$role" || true); \
							if [ -z "$$scope" ]; then \
								echo "[SKIP]: Role \`$$(basename $$collection)/$$(basename $$role)\` not staged." >  /dev/tty 2>&1; \
								continue; \
							fi; \
						fi; \
						echo "[INFO]: Testing role \`$$(basename $$collection)/$$(basename $$role)\`." >  /dev/tty 2>&1; \
						(cd "$$role" && molecule test) > /dev/tty 2>&1; \
					fi; \
				fi; \
			done; \
		fi; \
	done
