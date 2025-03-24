import shutil
from pathlib import Path

from .configs import ROOT_PATH, SYMLINKS_PATH, USER_HOME_PATH, Config, commit_updated_changes, is_windows

BACKUP_PATH = ROOT_PATH / "backups"


def update(is_simulator: bool = False, commit_message: str | None = None) -> None:
    """Update routine is executed after copy and with every update operation.

    :param is_simulator: simulator mode used for dev or testing, defaults to False
    """
    print(f"Executing update routine: {is_simulator=}")
    config = Config.from_json()
    config.echo()

    # Tasks
    replace_dotfiles_path()
    backup_then_symlink_dotfiles(config, is_simulator)
    if commit_message is None:
        template_version = get_latest_template_version()
        commit_message = f"Update to template version {template_version}"
    commit_updated_changes(commit_message)
    print("Update completed successfully!")


def replace_dotfiles_path() -> None:
    """Replace correct environment variable DOTFILES_PATH in profile."""
    string_to_replace = "REPLACE_DOTFILES_PATH_HERE"
    if is_windows():
        file_to_replace = SYMLINKS_PATH / "windows" / "PowerShell_profile.ps1"
    else:
        file_to_replace = SYMLINKS_PATH / "unix" / ".zsh_aliases"

    with open(file_to_replace, "r") as f:
        content = f.read()
    new_content = content.replace(string_to_replace, f"{SYMLINKS_PATH.as_posix()}")
    with open(file_to_replace, "w") as f:
        f.write(new_content)


def backup_then_symlink_dotfiles(config: Config, is_simulator: bool = False) -> None:
    """
    Backup and symlink dotfiles.
    By default dotfiles are symlinked to user $HOME folder.
    If is_simulator is True, dotfiles are symlinked to dotfiles parent folder instead.
    """
    symlink_sources = get_existing_symlink_sources()
    # Process symlinks
    for source_path, relative_path in symlink_sources:
        target_path = config.get_custom_symlink(source_path.name) or USER_HOME_PATH / relative_path
        # Avoid affecting real target path in simulator mode
        if is_simulator:
            target_path = SYMLINKS_PATH.parent / relative_path
        if target_path.exists():
            print(f"Backing up {target_path} to {BACKUP_PATH}")
            backup_path = BACKUP_PATH / relative_path
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target_path, backup_path)
            target_path.unlink()
        else:
            target_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"Symlinking: {source_path} -> {target_path}")
        target_path.symlink_to(source_path)
        config.active_symlinks[source_path.as_posix()] = target_path.as_posix()

    config.to_json()


### Backup and symlink methods
def get_existing_symlink_sources() -> list[tuple[Path, Path]]:
    """Get all existing symlink sources from common and os-specific folders."""
    common_path: Path = SYMLINKS_PATH / "common"
    os_specific_folder = "windows" if is_windows() else "unix"
    os_specific_path = SYMLINKS_PATH / os_specific_folder

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


def get_latest_template_version() -> str:
    import yaml

    """Get the latest template version from .copier-answers.yml."""
    copier_yml_path = SYMLINKS_PATH / ".copier-answers.yml"
    with open(copier_yml_path, "r") as file:
        return yaml.safe_load(file)["_commit"].strip()


if __name__ == "__main__":
    update()
