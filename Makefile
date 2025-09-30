# Makefile for Telegram Bot

# Variables
IMAGE_NAME = get-my-id-bot
CONTAINER_NAME = telegram-bot
ENV_FILE = .env

# Default target
.PHONY: help
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## Install dependencies using Poetry
	poetry install

.PHONY: dev
dev: ## Run bot in development mode
	poetry run python src/main.py

.PHONY: build
build: ## Build Docker image
	docker build -t $(IMAGE_NAME) .

.PHONY: run
run: ## Run bot in Docker container
	@if [ ! -f $(ENV_FILE) ]; then \
		echo "Error: $(ENV_FILE) file not found. Please copy env.example to .env and set your BOT_TOKEN"; \
		exit 1; \
	fi
	docker run --rm --env-file $(ENV_FILE) --name $(CONTAINER_NAME) $(IMAGE_NAME)

.PHONY: run-detached
run-detached: ## Run bot in Docker container (detached)
	@if [ ! -f $(ENV_FILE) ]; then \
		echo "Error: $(ENV_FILE) file not found. Please copy env.example to .env and set your BOT_TOKEN"; \
		exit 1; \
	fi
	docker run -d --env-file $(ENV_FILE) --name $(CONTAINER_NAME) $(IMAGE_NAME)

.PHONY: stop
stop: ## Stop running container
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

.PHONY: logs
logs: ## Show container logs
	docker logs -f $(CONTAINER_NAME)

.PHONY: shell
shell: ## Open shell in running container
	docker exec -it $(CONTAINER_NAME) /bin/bash

.PHONY: clean
clean: ## Clean up containers and images
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true
	docker rmi $(IMAGE_NAME) || true

.PHONY: setup-env
setup-env: ## Setup environment file from example
	@if [ ! -f $(ENV_FILE) ]; then \
		cp env.example $(ENV_FILE); \
		echo "Created $(ENV_FILE) from env.example. Please edit it and set your BOT_TOKEN."; \
	else \
		echo "$(ENV_FILE) already exists."; \
	fi

.PHONY: format
format: ## Format code using black
	poetry run black src/

.PHONY: lint
lint: ## Lint code using flake8
	poetry run flake8 src/

.PHONY: test
test: ## Run tests
	poetry run pytest

# Quick start commands
.PHONY: quick-start
quick-start: setup-env build run ## Quick start: setup env, build and run

.PHONY: quick-start-detached
quick-start-detached: setup-env build run-detached ## Quick start: setup env, build and run (detached)

.PHONY: quick-dev
quick-dev: install dev ## Quick development: install deps and run locally
