NAME := github-actions-kurobako
.DEFAULT_GOAL := help

IMAGE_NAME := "github-actions-kurobako"

.PHONY: docker-build
docker-build: ## Build docker image.
	docker build -t $(IMAGE_NAME) .

.PHONY: docker-sh
docker-sh: ## Open a bash shell in container for debugging.
	docker run -it --rm -v `PWD`/volume:/volume --entrypoint "sh" $(IMAGE_NAME)

.PHONY: help
help: ## Show help text
	@echo "Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

