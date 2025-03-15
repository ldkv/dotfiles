# Changelog

## Guidelines

https://keepachangelog.com/en/1.0.0/

**Added** for new features.\
**Changed** for changes in existing functionality.\
**Deprecated** for soon-to-be removed features.\
**Removed** for now removed features.\
**Fixed** for any bug fixes.\
**Security** in case of vulnerabilities.

## [Unreleased]

### Added

- Move files to subfolder `dotfiles_dir`
- Backup files before install to `backups` folder inside `dotfiles_dir`
- Script to setup the dotfiles once after the first copy:
  - Install `zsh` and `oh-my-zsh`
  - Backup then symlink the dotfiles
  - Initialize git repository

### Changed

- Rename template extension to `.j2` instead of `.jinja`

### Fixed

- Alias for `dotfiles-update` in .zshrc

## [0.0.4] - 2025-03-14

### Added

- gitignore template
- alias to update to latest template version

## [0.0.3] - 2025-03-14

### Changed

- Git init to $HOME directory

## [0.0.2] - 2025-03-14

### Added

- Possible to choose bare repository name for dotfiles

### Changed

- Update README.md

## [0.0.1] - 2025-03-14

### Added

- Initial Copier template
