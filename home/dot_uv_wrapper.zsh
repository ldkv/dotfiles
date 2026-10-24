# !/bin/zsh

export UV_CENTRAL_VENVS="$HOME/.local/share/uv_venvs"

function generate_hash() {
    # Generate Hash (using $PWD ensures uniqueness per folder)
    # We use 'echo -n' to avoid hashing the newline character
    if command -v md5 > /dev/null; then
        local project_hash=$(echo -n "$PWD" | md5)
    else
        local project_hash=$(echo -n "$PWD" | md5sum | awk '{print $1}')
    fi

    # Construct the target path
    local project_name=$(basename "$PWD")
    local target_venv="$UV_CENTRAL_VENVS/${project_name}-${project_hash}"
    echo "$target_venv"
}

function venv() {
    source $UV_PROJECT_ENVIRONMENT/bin/activate
}

function _auto_export_centralized_venv() {
    if [[ -f "pyproject.toml" ]]; then
        target_venv=$(generate_hash)
        export UV_PROJECT_ENVIRONMENT="$target_venv"
    fi
}

autoload -U add-zsh-hook
add-zsh-hook chpwd _auto_export_centralized_venv
_auto_export_centralized_venv
