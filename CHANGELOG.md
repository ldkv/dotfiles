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

## [0.4.0] - 2025-03-19

### Added

- Separate aliases to `.zsh_aliases`
- Python script to execute setup and update routines instead of shell scripts
- Configuration file `setup_configs.json` to configure the setup variables

### Changed

- Move dotfiles to separate folder for respective OS
- Move common dotfiles to `common` folder

### Removed

- Obsolete shell scripts

## [0.3.2] - 2025-03-16

### Changed

- Turns out the line is necessary in .zshrc

## [0.3.1] - 2025-03-16

### Changed

- Remove unnecessary line in .zshrc

## [0.3.0] - 2025-03-16

### Added

- Setup script for Windows using PowerShell v7

### Changed

- Move OMZ plugins and symlink target lists to `copier.yml` for easier maintenance
- Simplify Github actions with os matrix
- Use `uvx` to execute `copier` commands
- Adapt Makefile commands to support Windows
- Rename template files to adapt to Windows

## [0.2.2] - 2025-03-15

### Changed

- Evaluate aliases only once at setup

## [0.2.1] - 2025-03-15

### Fixed

- Aliases for `dotfiles` and `dotfiles-update` in `.zshrc`

## [0.2.0] - 2025-03-15

### Added

- New Github actions to test the complete setup
- Github actions now also runs on MacOS

### Changed

- Move all files outside of `dotfiles_dir`
- Adapt script to verify correct target directory before running
- Improve Makefile to support Github actions

## [0.1.3] - 2025-03-15

### Fixed

- Move `copier-answers` outside of `dotfiles_dir`

## [0.1.2] - 2025-03-15

### Changed

- Assume destination for symlink is parent directory of `dotfiles_dir`
- Rearrange .zshrc contents

## [0.1.1] - 2025-03-15

### Added

- Alias to move to dotfiles directory

### Fixed

- Alias dotfiles-update should work from any directory

## [0.1.0] - 2025-03-15

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
