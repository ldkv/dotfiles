import argparse
import os
import shutil
from pathlib import Path

from .configs import Config, commit_updated_changes, is_windows, run_command

USER_HOME_PATH = Path.home()
TEMPLATE_ROOT = Path(__file__).parent.parent.resolve()
OMZ_HOME = Path(os.environ.get("ZSH", USER_HOME_PATH / ".oh-my-zsh"))
OMZ_CUSTOM = Path(os.environ.get("ZSH_CUSTOM", OMZ_HOME / "custom"))


def setup(user_name: str, user_email: str) -> None:
    """Initialize setup for the first time."""
    print(f"Execute initial setup after first copy: {user_name=} {user_email=}")
    if is_windows():
        export_dotfiles_path_windows()
    else:
        install_zsh()
        install_oh_my_zsh()
        install_powerlevel10k()
        install_plugins()
        export_dotfiles_path_unix()

    init_git_repository(user_name, user_email)
    print("Setup completed successfully!")


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


def export_dotfiles_path_unix() -> None:
    """Append environment variable DOTFILES_PATH to .zshrc."""
    zshrc_path: Path = TEMPLATE_ROOT / "unix" / ".zshrc"
    with open(zshrc_path, "a") as f:
        f.write(f"export DOTFILES_PATH={TEMPLATE_ROOT}\n")


def export_dotfiles_path_windows() -> None:
    """Export environment variable DOTFILES_PATH for Windows."""
    profile_path = TEMPLATE_ROOT / "windows" / "PowerShell_profile.ps1"
    with open(profile_path, "a") as f:
        f.write("\n# For dotfiles\n")
        f.write(f'$env:DOTFILES_PATH = "{TEMPLATE_ROOT}"\n')
        f.write("function GotoDotfiles {cd $env:DOTFILES_PATH}\n")
        f.write("function DotfilesUpdate {uvx copier update $env:DOTFILES_PATH --trust -A}\n")
        f.write("Set-Alias dotfiles GotoDotfiles\n")
        f.write("Set-Alias dotfiles-update DotfilesUpdate\n")


def init_git_repository(user_name: str, user_email: str) -> None:
    """Initialize git repository if not already initialized."""
    if (TEMPLATE_ROOT / ".git").exists():
        print("git repository is already initialized.")
        return

    print("Initializing git repository...")
    run_command(f"git config --global user.name '{user_name}'")
    run_command(f"git config --global user.email '{user_email}'")
    run_command("git init .")
    commit_updated_changes("Initial commit with dotfiles template.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--user_name", type=str, required=True)
    parser.add_argument("--user_email", type=str, required=True)
    args = parser.parse_args()
    setup(args.user_name, args.user_email)
