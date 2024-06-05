.DEFAULT_GOAL := help

DOCKER_TAG = edwardcqian/ai-ml-workshop
BUILD_VERSION := latest
IMAGE_TAG = $(DOCKER_TAG):$(BUILD_VERSION)
VOLUMES = --mount type=bind,source=$(PWD),target=/home/jupyter
PORTS = -p 8888:8888

.PHONY: build
build: ## Build the lab Docker image containing all kernels.
	DOCKER_BUILDKIT=1 docker build \
	--build-arg BUILDKIT_INLINE_CACHE=1 \
	--cache-from $(DOCKER_TAG) \
	-f ./Dockerfile -t $(IMAGE_TAG) .

docker_run = docker run --rm -it  --entrypoint="" $(VOLUMES) $(IMAGE_TAG) $(1)

.PHONY: sh
sh: build ## Run and enter a bash shell in the lab container.
	$(call docker_run, bash)

.PHONY: fetch-assets
fetch-assets: ## Fetch the data for the workshop.
	curl -o data/data.txt https://storage.googleapis.com/edwardqian-dev/workshop/data.txt
	curl -o data/labelled_data.json https://storage.googleapis.com/edwardqian-dev/workshop/labelled_data.json
	curl -o models/pre_trained_model.pt https://storage.googleapis.com/edwardqian-dev/workshop/best_model.pt


.PHONY: lab
lab: build fetch-assets ## Run a JupyterLab server accessible on http://localhost:8888 in the lab container.
	docker run --rm $(VOLUMES) $(PORTS) $(IMAGE_TAG) \
		--Session.debug=false


.PHONY: help
help: ## Show help messages for make targets
	@grep -E '^[a-zA-\/Z_-]+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) \
		| sort \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}'