#!make

.PHONY: help

.DEFAULT_GOAL := help

help: ## show help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[$$()% 0-9a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Testing
copier: ## Install Copier
	uv tool install copier

TEMPLATE_FOLDER = home-simulator
template: copier ## Test the template generation process
	copier copy . $(TEMPLATE_FOLDER) --trust --vcs-ref=HEAD --force
	@echo "Template generated successfully in $(TEMPLATE_FOLDER)."

test-template: template ## Test the template generation process
	@rm -rf $(TEMPLATE_FOLDER)

test-template-ci: copier ## Test the template generation process without tasks for CI
	copier copy . $(TEMPLATE_FOLDER) --vcs-ref=HEAD --force --skip-tasks
	@rm -rf $(TEMPLATE_FOLDER)


##@ Release and Deployment
version: ## Get current project version
	$(eval version:=$(shell cat VERSION))
	@echo "Current version is: $(version)"

gh-release: version ## Release a new version using gh CLI
	gh release create $(version) --generate-notes


%:
	@true
