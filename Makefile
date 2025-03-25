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


##@ Scripts
SETUP_COMMAND = uv run -m src.setup
UPDATE_COMMAND = uv run -m src.update

setup: install_uv ## Setup the environment
	$(SETUP_COMMAND)
	$(UPDATE_COMMAND)

update: ## Backup then symlink dotfiles
	$(UPDATE_COMMAND)

simu-setup: install_uv ## Setup in simulator mode
	$(SETUP_COMMAND) --simulator

simu-update: ## Update in simulator mode
	$(UPDATE_COMMAND) --simulator


##@ Release and Deployment
bump: ## Commit version bump for production
	@if [ -z $(version) ]; then \
		echo "version not provided, skipping bump."; \
		echo "Example: make bump version=0.4.0"; \
		exit 1; \
	else \
		bump-my-version bump --new-version $(version) -vv; \
		git push; \
	fi

gh-release: bump ## Release a new version using gh CLI
	gh release create $(version) --generate-notes


%:
	@true
