import shutil
from pathlib import Path
from typing import NamedTuple

from .configs import DOTFILES_PATH, USER_HOME_PATH, Config, commit_updated_changes, is_windows


class SymlinkMapping(NamedTuple):
    source_path: Path
    relative_path: Path
    target_path: Path


def update(is_simulator: bool = False, commit_message: str | None = None) -> None:
    """Update routine is executed after copy and with every update operation.

    :param is_simulator: simulator mode used for dev or testing, defaults to False
    """
    print(f"Executing update routine: {is_simulator=}")
    configs = Config.from_json()
    configs.echo()

    # Tasks
    replace_dotfiles_path()
    symlink_mappings = generate_symlink_mappings(configs, is_simulator)
    backup_dotfiles(symlink_mappings)
    symlink_dotfiles(symlink_mappings)
    # Automatically commit updated changes
    if commit_message is None:
        template_version = get_latest_template_version()
        commit_message = f"Update to template version {template_version}"
    commit_updated_changes(commit_message)

    print("Update completed successfully!")


def replace_dotfiles_path() -> None:
    """Replace correct environment variable DOTFILES_PATH in profile."""
    string_to_replace = "REPLACE_DOTFILES_PATH_HERE"
    if is_windows():
        file_to_replace = DOTFILES_PATH / "windows" / "PowerShell_profile.ps1"
    else:
        file_to_replace = DOTFILES_PATH / "unix" / ".zsh_aliases"

    with open(file_to_replace, "r") as f:
        content = f.read()
    new_content = content.replace(string_to_replace, f"{DOTFILES_PATH.as_posix()}")
    with open(file_to_replace, "w") as f:
        f.write(new_content)


def backup_dotfiles(symlink_mappings: list[SymlinkMapping]) -> None:
    backup_dir = DOTFILES_PATH / "backups"
    for symlink in symlink_mappings:
        if not symlink.target_path.exists():
            print(f"Target path {symlink.target_path} doesn't exist, skipping backup")
            continue

        backup_path = backup_dir / symlink.relative_path
        print(f"Backing up {symlink.target_path} to {backup_path}")
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(symlink.target_path, backup_path)
        symlink.target_path.unlink()


def symlink_dotfiles(symlink_mappings: list[SymlinkMapping]) -> None:
    for symlink in symlink_mappings:
        target_path = symlink.target_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"Symlinking: {symlink.source_path} -> {target_path}")
        target_path.symlink_to(symlink.source_path)


def generate_symlink_mappings(config: Config, is_simulator: bool = False) -> list[SymlinkMapping]:
    """
    Generate all symlink mappings with target path.
    By default dotfiles are symlinked to user $HOME folder.
    In simulator mode, target paths point to a relative folder instead.
    """
    symlink_sources = get_existing_symlink_sources()
    symlink_mappings = []
    for source_path, relative_path in symlink_sources:
        target_path = config.get_custom_symlink(source_path.name) or USER_HOME_PATH / relative_path
        # Avoid affecting real target path in simulator mode
        if is_simulator:
            target_path = DOTFILES_PATH.parent / relative_path

        symlink_mappings.append(SymlinkMapping(source_path, relative_path, target_path))

    return symlink_mappings


def get_existing_symlink_sources() -> list[tuple[Path, Path]]:
    """Get all existing symlink sources from common and os-specific folders."""
    common_path = DOTFILES_PATH / "common"
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


def get_latest_template_version() -> str:
    import yaml

    """Get the latest template version from .copier-answers.yml."""
    copier_yml_path = DOTFILES_PATH / ".copier-answers.yml"
    with open(copier_yml_path, "r") as file:
        return yaml.safe_load(file)["_commit"].strip()


if __name__ == "__main__":
    update()
