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

function uv() {
    # List of uv commands that require/interact with an environment
    local venv_commands=("sync" "run" "add" "remove" "build" "publish" "lock" "tree" "format" "pip")

    # ${venv_commands[(r)$1]} is Zsh specific syntax to check existence in array
    # Pass through commands like 'uv tool', 'uv self', 'uv python' directly
    if [[ ${venv_commands[(r)$1]} == "$1" ]]; then
        mkdir -p "$UV_CENTRAL_VENVS"
        local target_venv=$(generate_hash)
        UV_PROJECT_ENVIRONMENT="$target_venv" command uv "$@"
    else
        command uv "$@"
    fi
}

function venv() {
    local target_venv=$(generate_hash)
    source ${target_venv}/bin/activate
}
