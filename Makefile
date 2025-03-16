#!make

.PHONY: help template

.DEFAULT_GOAL := help

help: ## show help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[$$()% 0-9a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Pre-requisites
install_uv: ## Install uv
	@if ! uv -V ; then \
        echo "uv not found, installing..."; \
        curl -LsSf https://astral.sh/uv/install.sh | sh; \
		source $(HOME)/.cargo/env ; \
    else \
        echo "uv is already installed. Skipped."; \
    fi

install_copier: install_uv ## Install Copier
	uv tool install copier


##@ Development and Testing
SIMULATOR_FOLDER=home-simulator
COPIER_COMMAND=uvx copier copy --vcs-ref=HEAD --force --trust .
template: remove-template ## Generate the template for development
	$(COPIER_COMMAND) $(SIMULATOR_FOLDER)/.dotfiles -d 'simulator=true'
	@echo "Template generated successfully in $(SIMULATOR_FOLDER)."

remove-template: ## Remove the generated template
	rm -r -f $(SIMULATOR_FOLDER);
	@echo "Template removed successfully."

test-template: install_copier ## Test complete template generation with tasks
	$(COPIER_COMMAND) $(HOME)/.dot

test-template-no-tasks: install_copier ## Test template generation without tasks
	$(COPIER_COMMAND) $(HOME)/.dot --skip-tasks


##@ Release and Deployment
version: ## Get current project version
	$(eval version:=$(shell cat VERSION))
	@echo "Current version is: $(version)"

gh-release: version ## Release a new version using gh CLI
	gh release create $(version) --generate-notes


%:
	@true
