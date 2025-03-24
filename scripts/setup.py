import argparse
import os
import shutil
from pathlib import Path

from .configs import SYMLINKS_PATH, USER_HOME_PATH, Config, is_windows, run_command

OMZ_HOME = Path(os.environ.get("ZSH", USER_HOME_PATH / ".oh-my-zsh"))
OMZ_CUSTOM = Path(os.environ.get("ZSH_CUSTOM", OMZ_HOME / "custom"))


def setup(is_simulator: bool = False) -> None:
    print(f"Execute initial setup after first copy: {is_simulator=}")
    config = Config.from_json()
    config.echo()

    # Tasks
    if not is_windows():
        install_zsh()
        install_oh_my_zsh()
        install_powerlevel10k_theme()
        install_omz_plugins(config.omz_plugins)

    print("Setup completed successfully!")
    # update(is_simulator, "Initial commit with dotfiles template.")


def install_zsh() -> None:
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
    if OMZ_HOME.exists():
        print("oh-my-zsh is already installed. Skipped.")
        return

    print("Installing oh-my-zsh...")
    run_command('sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"')


def install_powerlevel10k_theme() -> None:
    theme_path: Path = OMZ_CUSTOM / "themes" / "powerlevel10k"
    if theme_path.exists():
        print("powerlevel10k theme is already installed. Skipped.")
        return

    print("Installing powerlevel10k theme...")
    run_command(f"git clone --depth=1 https://github.com/romkatv/powerlevel10k.git {theme_path}")


def install_omz_plugins(omz_plugins: dict[str, str]) -> None:
    for plugin_name, plugin_url in omz_plugins.items():
        plugin_path: Path = OMZ_CUSTOM / "plugins" / plugin_name
        if plugin_path.exists():
            print(f"{plugin_name} plugin is already installed. Skipped.")
            continue

        print(f"Installing {plugin_name} plugin...")
        run_command(f"git clone {plugin_url} {plugin_path}")


def init_git_repository() -> None:
    """Initialize git repository if not already initialized."""
    if (SYMLINKS_PATH / ".git").exists():
        print("git repository is already initialized.")
        return

    print("Initializing git repository...")
    run_command("git init .")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulator", action="store_true")
    args = parser.parse_args()
    setup(args.simulator)
