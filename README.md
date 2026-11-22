# dotfiles

My dotfiles for Linux, macOS and Windows, managed with [chezmoi](https://www.chezmoi.io/).

## What it sets up

- **Linux / macOS**: zsh as login shell, [Oh My Zsh](https://ohmyz.sh/), [powerlevel10k](https://github.com/romkatv/powerlevel10k), zsh-autosuggestions, fast-syntax-highlighting and ohmyzsh-full-autoupdate.
- **Windows**: PowerShell 7 profile.
- **Everywhere**: `.gitconfig`, `.taskrc.yml` and `Taskfile.yml` in `~/dev` (Windows: `D:\dev`).

## Prerequisites

- Linux / macOS: `git`, `curl` and [uv](https://docs.astral.sh/uv/), plus `apt` or `brew` to install zsh.
- Windows: PowerShell 7, [scoop](https://scoop.sh), and `starship`, `git-aliases`, `task` and [uv](https://docs.astral.sh/uv/) used by the profile.

To install `uv`, run:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Install on a new machine

Linux / macOS:

```bash
sh -c "$(curl -fsLS get.chezmoi.io)" -- -b ~/.local/bin init --apply ldkv/dotfiles
```

Windows:

```powershell
scoop install chezmoi
chezmoi init --apply ldkv/dotfiles
```

> [!TIP]
> On a machine that already has dotfiles, run `chezmoi init ldkv/dotfiles` then `chezmoi diff` to review changes before `chezmoi apply`.

`chezmoi init` asks once per machine:

| Prompt       | Used for                | Default          |
| ------------ | ----------------------- | ---------------- |
| `user_name`  | git `user.name`         | Vu LE            |
| `user_email` | git `user.email`        | ledkvu@gmail.com |
| `is_wsl`     | WSL-specific `$BROWSER` | false            |

To change an answer later, edit `~/.config/chezmoi/chezmoi.toml` (`chezmoi edit-config`).

## Daily use

| Command                  | Alias             | What it does                                         |
| ------------------------ | ----------------- | ---------------------------------------------------- |
| `chezmoi update`         | `dotfiles-update` | Pull the latest changes and apply them               |
| `chezmoi cd`             |                   | Open a shell in the source repo                      |
|                          | `dotfiles`        | `cd` to the source repo                              |
| `chezmoi edit ~/.zshrc`  |                   | Edit the source of a file, then `chezmoi apply`      |
| `chezmoi re-add`         |                   | Copy local edits of non-templated files back to repo |
| `chezmoi diff`           |                   | Show what `chezmoi apply` would change               |
| `chezmoi merge ~/.zshrc` |                   | Resolve a file edited both locally and in the repo   |

Changes made through chezmoi are committed automatically; push them from `chezmoi cd`.

## Layout

| Path                                  | Purpose                                                                    |
| ------------------------------------- | -------------------------------------------------------------------------- |
| `home/`                               | chezmoi source directory (see `.chezmoiroot`)                              |
| `home/.chezmoi.toml.tmpl`             | Per-machine prompts                                                        |
| `home/.chezmoiexternal.toml.tmpl`     | Oh My Zsh, powerlevel10k and plugins (cloned once)                         |
| `home/.chezmoiignore`                 | Per-OS ignores                                                             |
| `home/.chezmoidata/outside_home.yaml` | Windows files copied outside `$HOME` or to runtime paths (e.g. `$PROFILE`) |
| `home/run_onchange_*`                 | zsh install and Windows outside-`$HOME` deploy scripts                     |

## Development

```bash
task test  # apply into a sandbox HOME (.sandbox/) without running scripts
```

CI applies the dotfiles on Ubuntu, macOS and Windows and checks that the shell starts without errors.
