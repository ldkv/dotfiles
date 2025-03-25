import dataclasses
import json
import os
import platform
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

SYSTEM_OS = platform.system().lower()
PYTHON_VERSION = sys.version
USER_HOME_PATH = Path.home()
SCRIPTS_PATH = Path(__file__).parent.resolve()
ROOT_PATH = SCRIPTS_PATH.parent


@dataclass
class Config:
    omz_plugins: dict[str, str]
    custom_symlinks: dict[str, dict[str, str]]
    active_symlinks: dict[str, str] = dataclasses.field(default_factory=dict)

    @classmethod
    def path(cls) -> Path:
        file_name = "configs.json"
        return ROOT_PATH / file_name

    @classmethod
    def from_json(cls) -> "Config":
        """Load configurations from JSON file."""
        config_path = cls.path()
        with open(config_path, "r") as f:
            raw_config = json.load(f)

        return cls(**raw_config)

    def to_json(self) -> None:
        """Save current configurations to JSON file."""
        config_path = self.path()
        with open(config_path, "w") as f:
            json.dump(dataclasses.asdict(self), f, indent=2)

    def echo(self) -> None:
        print(f"System settings: {SYSTEM_OS=} | {PYTHON_VERSION=} | {SCRIPTS_PATH=} | {USER_HOME_PATH=}")
        print(f"Active configurations: {self}")

    def get_custom_symlink(self, source_name: str) -> Path | None:
        dest_path = self.custom_symlinks.get(SYSTEM_OS, {}).get(source_name)
        if not dest_path:
            return None

        if dest_path.startswith("$"):
            dest_path = get_env_var(dest_path[1:])

        return Path(dest_path)


def get_env_var(var_name: str) -> str | None:
    if not is_windows():
        return os.environ[var_name]

    # In windows env_var may be $env:DOTFILES_PATH or $DOTFILES_PATH
    for prefix in ["$env:", "$"]:
        env_val = run_command(f'pwsh -c "echo {prefix}{var_name}"')
        if env_val:
            return env_val

    return None


def is_windows() -> bool:
    """Check if the current system is Windows."""
    return SYSTEM_OS == "windows"


def run_command(cmd: str, check: bool = True) -> str | None:
    """Run a shell command and return its output."""
    try:
        result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{cmd}': {e}")
        if check:
            raise
        return None


def commit_updated_changes(message: str) -> None:
    """Commit changes to git repository."""
    run_command("git add .")
    staged_files = run_command("git diff --staged --name-only").split("\n")
    staged_files = [file for file in staged_files if file]
    if not staged_files:
        print("No changes to commit. Skipped.")
        return

    print(f"Committing changes for {staged_files=} with {message=}")
    run_command(f'git commit -m "{message}"')
