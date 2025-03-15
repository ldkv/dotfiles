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

Install `copier` using `uv` tool:

```bash
uv tool install copier
```

## Features

The template includes the following features:

- [x] Use [uv](https://docs.astral.sh/uv/) as project and dependencies manager
- [x] To be defined

## How to use

### Initialize and merge with your dotfiles

> [!CAUTION]
> Merging may overwrite existing files, make sure to backup your own dotfiles before merging.

To merge your dotfiles using this template, run:

```bash
copier copy gh:ldkv/dotfiles.git $HOME --skip-tasks
```

This command will copy the template to your home directory and skip all oneshot tasks, which are to install oh-my-zsh and its plugins.

If you trust the template and want to execute all tasks, run the following command instead:

```bash
copier copy gh:ldkv/dotfiles.git $HOME --trust
```

Then follow the on-screen instructions to resolve conflicts with existing files.

### Update the project with latest template version

After a project is already configured with this template, a file `.copier-answers.yml` should be generated in the project root directory. Do NOT modify this file manually.

To update the project with the latest template version, simply run:

```bash
copier update -A
```

## Contributing

To contribute to this template, feel free to open an issue or submit a pull request.
