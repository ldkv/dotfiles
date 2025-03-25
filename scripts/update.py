import argparse
import shutil
from pathlib import Path
from typing import NamedTuple

from scripts.configs import ROOT_PATH, USER_HOME_PATH, Config, is_windows


class SymlinkMapping(NamedTuple):
    source_path: Path
    relative_path: Path
    target_path: Path

    @staticmethod
    def symlinks_path() -> Path:
        return ROOT_PATH / "symlinks"


def update(is_simulator: bool = True) -> None:
    """Routine to backup and symlink existing dotfiles.

    :param is_simulator: simulator mode used for dev or testing, defaults to False
    """
    print(f"Executing update routine: {is_simulator=}")
    configs = Config.from_json()
    configs.echo()

    target_dir = None
    backup_dir = ROOT_PATH / "backups"
    if is_simulator:
        simulator_dir = ROOT_PATH / "home-simulator"
        target_dir = simulator_dir / "symlinks"
        backup_dir = simulator_dir / "backups"

    symlink_mappings = generate_symlink_mappings(configs, target_dir)

    backup_dotfiles(symlink_mappings, backup_dir)
    symlink_dotfiles(symlink_mappings)
    print("Update completed successfully!")


def backup_dotfiles(symlink_mappings: list[SymlinkMapping], backup_dir: Path) -> None:
    """
    Backup dotfiles.
    """
    for symlink in symlink_mappings:
        if not symlink.target_path.exists():
            print(f"Skipping backup for {symlink.target_path} because it doesn't exist")
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


def generate_symlink_mappings(config: Config, simulator_dir: Path | None = None) -> list[SymlinkMapping]:
    """
    Generate all symlink mappings with target path.
    By default dotfiles are symlinked to user $HOME folder.
    In simulator mode, target paths point to a relative folder instead.
    """
    symlink_sources = get_existing_symlink_sources()
    symlink_mappings = []
    for source_path, relative_path in symlink_sources:
        if simulator_dir:
            target_path = simulator_dir / relative_path
        else:
            target_path = config.get_custom_symlink(source_path.name) or USER_HOME_PATH / relative_path

        symlink_mappings.append(SymlinkMapping(source_path, relative_path, target_path))

    return symlink_mappings


def get_existing_symlink_sources() -> list[tuple[Path, Path]]:
    """Get all existing symlink sources from common and os-specific folders."""
    symlinks_path = SymlinkMapping.symlinks_path()
    common_path = symlinks_path / "common"
    os_specific_folder = "windows" if is_windows() else "unix"
    os_specific_path = symlinks_path / os_specific_folder

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulator", action="store_true")
    args = parser.parse_args()
    update(args.simulator)
