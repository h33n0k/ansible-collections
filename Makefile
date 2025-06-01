# Variables
SHELL := /bin/bash
PYTHON := python3
VENV_DIR := venv
COLLECTIONS_BASE := collections/ansible_collections/h33n0k
COLLECTIONS := $(wildcard $(COLLECTIONS_BASE)/*)
COMMAND ?= test

.PHONY: help init prepare lint test

help: ## Show help for each command
	@echo "Usage: make <target> [VAR=value]"
	@echo
	@echo -e "\033[1;37mTargets:\033[0m"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m \033[2;37m%s\033[0m\n", $$1, $$2}'
	@echo
	@echo -e "\033[1;37mOptional vars:\033[0m"
	@echo -e "  \033[33mROLE\033[0m=namespace/role_name     \033[2;37m# Filter by role name (e.g. tools/docker)\033[0m"
	@echo -e "  \033[33mCOMMAND\033[0m=test                 \033[2;37m# Molecule command (e.g. create, converge, verify)\033[0m"
	@echo -e "  \033[33mSTAGED_ONLY\033[0m=true             \033[2;37m# Run only on staged roles\033[0m"
	@echo -e "  \033[33mCHANGED_SINCE\033[0m=<commit>       \033[2;37m# Only test roles changed since this commit (e.g. latest merge base)\033[0m"
	@echo -e "  \033[33mBASE_BRANCH\033[0m=<branch>         \033[2;37m# Base branch to compare against for changes (default: origin/main)\033[0m"


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

test: ## Run molecule command on specific roles
	@for collection in $(COLLECTIONS); do \
		roles_dir="$$collection/roles"; \
		if [ -d "$$roles_dir" ]; then \
			for role in $$roles_dir/*; do \
				if [ -n "$(ROLE)" ]; then \
					[ "$$(basename $$collection)/$$(basename $$role)" != "$(ROLE)" ] && continue; \
				fi; \
				if [ -d "$$role" ]; then \
					name="$$(basename $$collection)/$$(basename $$role)"; \
					scenarios="$$(find $$role -type f -iname molecule.yml)"; \
					if [ ! -z "$$scenarios" ]; then \
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
						for scenario in "$${scenarios[@]}"; do \
							s_name="$$(basename $$(dirname $$scenario))"; \
							echo "[INFO]: Testing role \`$$name\` [$$s_name]."; \
							(cd "$$role" && molecule "$(COMMAND)" --scenario-name "$$s_name"); \
						done; \
					fi; \
				fi; \
			done; \
		fi; \
	done
