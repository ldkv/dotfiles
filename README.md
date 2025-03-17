[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-orange.json)](https://github.com/copier-org/copier)

# dotfiles

## About

A [Copier](https://copier.readthedocs.io/en/stable/) template to generate and sync dotfiles for various environments.

## Prerequisites

The project template is generated with [Copier](https://copier.readthedocs.io/en/stable/) and powered by [uv](https://docs.astral.sh/uv/).

To install `uv`, run:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then install `copier` using `uv` tool:

```bash
uv tool install copier
```

## Features

This template includes the following features:

- [x] TBD

## How to use

### Initialize and symlink to your dotfiles

To initialize this template, run:

```bash
uvx copier copy gh:ldkv/dotfiles.git $HOME/.dotfiles --trust
```

> [!CAUTION]
> The target directory must be a subfolder of the home directory, e.g. `$HOME/.dotfiles`.

This command will copy the template to the target directory, then execute the initial setup script to do the following actions in order. The action will be skipped if already done:

- Install `zsh`
- Install [Oh My Zsh](https://ohmyz.sh/)
- Install [powerlevel10k theme](https://github.com/romkatv/powerlevel10k)
- Install various zsh plugins
- Backup supported dotfiles to `$HOME/.dotfiles/backups`
- Symlink dotfiles to the home directory
- Initialize git repository in the target directory and then make first commit

It is also possible to execute the script yourself after initializing the template, by running:

```bash
uvx copier copy gh:ldkv/dotfiles.git $HOME/.dotfiles --skip-tasks
cd $HOME/.dotfiles
chmod +x setup_once.sh
./setup_once.sh
```

### Update the project with latest template version

After a project is already configured with this template, a file `.copier-answers.yml` should be generated in the project root directory. Do NOT modify this file manually.

To update the project with the latest template version, simply run:

```bash
uvx copier update -A --skip-tasks
```

Or using the existing alias:

```bash
dotfiles-update
```

## Contributing

To contribute to this template, feel free to open an issue or submit a pull request.
