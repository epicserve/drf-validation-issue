# For more information on the following see http://clarkgrubb.com/makefile-style-guide
MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help
.DELETE_ON_ERROR:
.SUFFIXES:

HELP_FIRST_COL_LENGTH := 23

# COLORS
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)
TARGET_MAX_CHAR_NUM := 23

.PHONY: help
help:
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-$(TARGET_MAX_CHAR_NUM)s$(RESET)$(GREEN)%s$(RESET)\n", $$1, $$2}'
	@echo ''

.PHONY: fix_py_imports
fix_py_imports: ## Fix Python imports with isort
	@isort --recursive .

.PHONY: lint_py
lint_py: ## Lint Python code flake8
	@echo "Checking code using flake8 ..."
	@flake8 --ignore E501

.PHONY: lint_imports
lint_imports: ## Lint Python imports with isort
	@echo "Checking python imports ..."
	@isort --recursive --check-only --diff .

.PHONY: lint
lint: lint_py lint_imports ## Lint Python and Python imports

.PHONY: test
test: ## Run tests with pytest
	@pytest
