#!/usr/bin/env python3
import argparse
import dataclasses
import json
import os
import platform
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

SYSTEM_OS = platform.system().lower()
USER_HOME_PATH = Path.home()
DOTFILES_PATH = Path(__file__).parent.resolve()
BACKUP_PATH = DOTFILES_PATH / "backups"
OMZ_HOME = Path(os.environ.get("ZSH", USER_HOME_PATH / ".oh-my-zsh"))
OMZ_CUSTOM = Path(os.environ.get("ZSH_CUSTOM", OMZ_HOME / "custom"))


@dataclass
class Config:
    omz_plugins: dict[str, str]
    custom_symlinks: dict[str, dict[str, str]]
    active_symlinks: dict[str, str] = dataclasses.field(default_factory=dict)

    @classmethod
    def path(cls) -> Path:
        file_name = "setup_configs.json"
        return DOTFILES_PATH / file_name

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

    def get_custom_symlink(self, source_name: str) -> Path | None:
        dest_path = self.custom_symlinks.get(SYSTEM_OS, {}).get(source_name)
        if not dest_path:
            return None

        if dest_path.startswith("$"):
            dest_path = os.environ[dest_path[1:]]  # should raise KeyError if not found

        return Path(dest_path)


def is_windows() -> bool:
    """Check if the current system is Windows."""
    return SYSTEM_OS == "windows"


def run_command(cmd: str, check: bool = True) -> str | None:
    """Run a shell command and return its output."""
    try:
        result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{cmd}': {e}")
        if check:
            raise
        return None


### Initial setup methods for Unix systems
def install_zsh() -> None:
    """Install zsh if not already installed."""
    if shutil.which("zsh"):
        print("zsh is already installed. Skipped.")
        return

    print("Installing zsh...")
    if shutil.which("apt"):
        run_command("sudo apt update")
        run_command("sudo apt install -y zsh")
        return

    if shutil.which("brew"):
        run_command("brew install zsh")
        return

    raise Exception("Unsupported package manager. Please install zsh manually.")


def install_oh_my_zsh() -> None:
    """Install oh-my-zsh if not already installed."""
    if OMZ_HOME.exists():
        print("oh-my-zsh is already installed. Skipped.")
        return

    print("Installing oh-my-zsh...")
    run_command('sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"')


def install_powerlevel10k() -> None:
    """Install powerlevel10k theme if not already installed."""
    theme_path: Path = OMZ_CUSTOM / "themes" / "powerlevel10k"
    if theme_path.exists():
        print("powerlevel10k theme is already installed. Skipped.")
        return

    print("Installing powerlevel10k theme...")
    run_command(f"git clone --depth=1 https://github.com/romkatv/powerlevel10k.git {theme_path}")


def install_plugins() -> None:
    """Install oh-my-zsh plugins."""
    config = Config.from_json()
    for plugin_name, plugin_url in config.omz_plugins.items():
        plugin_path: Path = OMZ_CUSTOM / "plugins" / plugin_name
        if plugin_path.exists():
            print(f"{plugin_name} plugin is already installed. Skipped.")
            continue

        print(f"Installing {plugin_name} plugin...")
        run_command(f"git clone {plugin_url} {plugin_path}")


def export_dotfiles_path() -> None:
    """Append environment variable DOTFILES_PATH to .zshrc."""
    zshrc_path: Path = DOTFILES_PATH / "unix" / ".zshrc"
    with open(zshrc_path, "a") as f:
        f.write(f"export DOTFILES_PATH={DOTFILES_PATH}\n")


### Backup and symlink methods
def get_existing_symlink_sources() -> list[tuple[Path, Path]]:
    """Get all existing symlink sources from common and os-specific folders."""
    common_path: Path = DOTFILES_PATH / "common"
    os_specific_folder = "windows" if is_windows() else "unix"
    os_specific_path = DOTFILES_PATH / os_specific_folder

    return get_all_files_in_folder(common_path) + get_all_files_in_folder(os_specific_path)


def get_all_files_in_folder(folder_path: Path) -> list[tuple[Path, Path]]:
    """
    Get all files in a folder. Return the absolute path and the path relative to the folder path.
    Example:
        folder_path: /dotfiles/unix
        files & subfolders:
            - .p10k.zsh
            - nested/.zshrc
        return: [
            (/dotfiles/unix/.p10k.zsh, .p10k.zsh),
            (/dotfiles/unix/nested/.zshrc, nested/.zshrc),
        ]
    """
    return [(file.absolute(), file.relative_to(folder_path)) for file in folder_path.glob("**/*") if file.is_file()]


def backup_then_symlink_dotfiles(is_simulator: bool = False) -> None:
    """
    Backup and symlink dotfiles.
    By default dotfiles are symlinked to user $HOME folder.
    If is_simulator is True, dotfiles are symlinked to dotfiles parent folder instead.
    """
    config = Config.from_json()
    symlink_sources = get_existing_symlink_sources()
    target_dir = DOTFILES_PATH.parent if is_simulator else USER_HOME_PATH
    # Process symlinks
    for source_path, relative_path in symlink_sources:
        target_path = config.get_custom_symlink(source_path.name) or target_dir / relative_path
        if target_path.exists():
            print(f"Backing up {target_path} to {BACKUP_PATH}")
            backup_path = BACKUP_PATH / target_path.relative_to(target_dir)
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target_path, backup_path)
            target_path.unlink()
        else:
            target_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"Symlinking: {target_path} -> {source_path}")

        target_path.symlink_to(source_path)
        config.active_symlinks[source_path.as_posix()] = target_path.as_posix()

    config.to_json()


### Git methods
def init_git_repo() -> None:
    """Initialize git repository if not already initialized."""
    if (DOTFILES_PATH / ".git").exists():
        print("git repository is already initialized.")
        return

    print("Initializing git repository...")
    run_command("git init .")
    commit_updated_changes("Init dotfiles template")


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


### Setup and update routines
def setup() -> None:
    """Initialize setup for the first time."""
    print(f"Executing setup routine for {SYSTEM_OS=}.")
    if not is_windows():
        install_zsh()
        install_oh_my_zsh()
        install_powerlevel10k()
        install_plugins()
        export_dotfiles_path()

    init_git_repo()


def update(version: str = "undefined", is_simulator: bool = False) -> None:
    """Update routine is executed after copy and with every update operation.

    :param is_simulator: simulator mode used for dev or testing, defaults to False
    """
    print(f"Executing update routine for {SYSTEM_OS=} | {is_simulator=}.")
    backup_then_symlink_dotfiles(is_simulator)
    commit_updated_changes(f"Update to template version {version}")


def main() -> None:
    """Main function to run all setup steps."""
    # Get args
    parser = argparse.ArgumentParser()
    parser.add_argument("--setup", action="store_true")
    parser.add_argument("--update", action="store_true")
    parser.add_argument("--version", type=str, default="undefined")
    parser.add_argument("--simulator", action="store_true")
    args = parser.parse_args()
    print(f"Input args: {args}")

    operation = "Setup" if args.setup else "Update"
    if args.setup:
        setup()
    if args.update:
        update(args.version, args.simulator)
    print(f"{operation} completed successfully!")


if __name__ == "__main__":
    main()
