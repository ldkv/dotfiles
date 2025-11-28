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
SIMULATOR_DIR=home-simulator
COPIER_COMMAND=uvx copier copy --vcs-ref=HEAD --force --trust .
template: remove-template ## Generate the template for development
	$(COPIER_COMMAND) $(SIMULATOR_DIR)/.dotfiles -d 'simulator=true'
	@echo "Template generated successfully in $(SIMULATOR_DIR)."

remove-template: ## Remove the generated template
	rm -r -f $(SIMULATOR_DIR);
	@echo "Template removed successfully."

test-template: install_copier ## Test complete template generation with tasks
	$(COPIER_COMMAND) $(HOME)/.dot

test-template-no-tasks: install_copier ## Test template generation without tasks
	$(COPIER_COMMAND) $(HOME)/.dot --skip-tasks


##@ Release and Deployment
PROD_DIR=prod
PROD_COMMAND=uvx copier copy --trust .
copy-template: ## Initialize the template as a subfolder
	$(PROD_COMMAND) $(PROD_DIR)

update-template: ## Update the production template
	uvx copier update $(PROD_DIR) --trust -A

bump: ## Commit version bump for production
	@if [ -z $(version) ]; then \
		echo "version not provided, skipping bump."; \
		echo "Example: make bump version=0.4.0"; \
		exit 1; \
	else \
		uvx bump-my-version bump --new-version $(version) -vv; \
		git push; \
	fi

gh-release: bump ## Release a new version using gh CLI
	git push --tags
	gh release create $(version) --generate-notes


%:
	@true
