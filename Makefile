# Variables
SHELL := /bin/bash
PYTHON := python3
VENV_DIR := venv
COLLECTIONS_BASE := collections/ansible_collections/h33n0k
COLLECTIONS := $(wildcard $(COLLECTIONS_BASE)/*)

.PHONY: help init prepare lint test

help: ## Show help for each command
	@echo "Usage: make <target> [VAR=value]"
	@echo
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'
	@echo
	@echo "Optional vars:"
	@echo "  ROLE=namespace/role_name     Filter by role name"
	@echo "  STAGED_ONLY=true             Run only on staged roles"
	@echo "  CHANGED_SINCE=<commit>        Only test roles changed since this commit (e.g. latest merge base)"
	@echo "  BASE_BRANCH=<branch>         Base branch to compare against for changes (default: origin/main)"


init: ## Create virtualenv
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV_DIR)

	@echo "Virtual environment created. Run the following to activate it:"
	@echo "source $(VENV_DIR)/bin/activate"
	@echo "---"

prepare: ## Install dev and Ansible galaxy dependencies
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

lint: ## Lint all roles
	@echo "Linting codebase"
	ansible-lint $(COLLECTIONS_BASE)

test: ## Run molecule test on all or specific roles
	@for collection in $(COLLECTIONS); do \
		roles_dir="$$collection/roles"; \
		if [ -d "$$roles_dir" ]; then \
			for role in $$roles_dir/*; do \
				if [ -n "$(ROLE)" ]; then \
					[ "$$(basename $$collection)/$$(basename $$role)" != "$(ROLE)" ] && continue; \
				fi; \
				if [ -d "$$role" ]; then \
					config="$$role/molecule/default/molecule.yml"; \
					name="$$(basename $$collection)/$$(basename $$role)"; \
					if [ -f "$$config" ]; then \
						if [ "$(STAGED_ONLY)" = "true" ]; then \
							scope=$$(git diff --cached --name-only | grep "^$$role" || true); \
							if [ -z "$$scope" ]; then \
								echo "[SKIP]: Role \`$$name\` not staged."; \
								continue; \
							fi; \
						elif [ -n "$(CHANGED_SINCE)" ]; then \
							base_branch="$${BASE_BRANCH:-origin/main}"; \
							changed=$$(git diff --name-only "$$base_branch...$(CHANGED_SINCE)" | grep "^$$role" || true); \
							if [ -z "$$changed" ]; then \
								echo "[SKIP]: Role \`$$name\` unchanged since \`$(CHANGED_SINCE)\`."; \
								continue; \
							fi; \
						fi; \
						echo "[INFO]: Testing role \`$$name\`."; \
						(cd "$$role" && molecule test); \
					fi; \
				fi; \
			done; \
		fi; \
	done
