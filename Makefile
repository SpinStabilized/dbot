# Makefile for dbot project

run: ## Run from python source
	@echo "Starting dbot from source"
	@python src/dbot.py
.PHONY: run

freeze: ## Freeze the build dependencies to requirements.txt
	@echo "Freezing build depdencies to requirements.txt"
	@pipenv requirements > requirements.txt

build: freeze ## Build and launch container
	@echo "Building and launching container for debugging."
	@docker-compose -f "docker-compose.yml" up -d --build
.PHONY: build

build_debug: freeze ## Build and launch container with python debugger port available
	@echo "Building and launching container for debugging."
	@docker-compose -f "docker-compose.debug.yml" up -d --build
.PHONY: build_debug

help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
.PHONY: help
.DEFAULT_GOAL = help