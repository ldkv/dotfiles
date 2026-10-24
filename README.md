# dotfiles

My dotfiles for Linux (apt), macOS and Windows, managed with [chezmoi](https://www.chezmoi.io/).

## What it sets up

- **Linux / macOS**: zsh as login shell, [Oh My Zsh](https://ohmyz.sh/), [powerlevel10k](https://github.com/romkatv/powerlevel10k), zsh-autosuggestions, fast-syntax-highlighting, `gh`, `task` and `uv`.
- **Windows**: PowerShell 7 profile with starship, git-aliases, `gh`, `task` (via [scoop](https://scoop.sh)) and `uv`.
- **Everywhere**: `.gitconfig`, `.taskrc.yml`, a `Taskfile.yml` in your dev folder, VS Code and Zed `settings.json`.

## Install on a new machine

Linux / macOS:

```bash
sh -c "$(curl -fsLS get.chezmoi.io)" -- -b ~/.local/bin init --apply ldkv/dotfiles
```

Windows (PowerShell 7, [scoop](https://scoop.sh) installed, [Developer Mode](https://learn.microsoft.com/en-us/windows/apps/get-started/enable-your-device-for-development) enabled for symlinks):

```powershell
scoop install chezmoi
chezmoi init --apply ldkv/dotfiles
```

> [!TIP]
> On a machine that already has dotfiles, run `chezmoi init ldkv/dotfiles` then `chezmoi diff` to review changes before `chezmoi apply`.

`chezmoi init` asks once per machine:

| Prompt       | Used for                                    | Default                             |
| ------------ | ------------------------------------------- | ----------------------------------- |
| `user_name`  | git `user.name`                             | Vu LE                               |
| `user_email` | git `user.email`                            | ledkvu@gmail.com                    |
| `dev_dir`    | where `Taskfile.yml` is copied, `$env:DEV`  | `~/dev` (Windows: `D:\dev`)         |
| `editor`     | git `core.editor`                           | `code --wait`                       |

WSL is detected automatically. To change an answer later, edit `~/.config/chezmoi/chezmoi.toml` (`chezmoi edit-config`).

## Daily use

| Command                  | Alias             | What it does                                         |
| ------------------------ | ----------------- | ---------------------------------------------------- |
| `chezmoi update`         | `dotfiles-update` | Pull the latest changes and apply them               |
| `chezmoi cd`             | `dotfiles`        | Open a shell in the source repo                      |
| `chezmoi edit ~/.zshrc`  |                   | Edit the source of a file, then `chezmoi apply`      |
| `chezmoi re-add`         |                   | Copy local edits of non-templated files back to repo |
| `chezmoi diff`           |                   | Show what `chezmoi apply` would change               |
| `chezmoi merge ~/.zshrc` |                   | Resolve a file edited both locally and in the repo   |

Changes made through chezmoi are committed automatically; push them from `chezmoi cd`.

VS Code and Zed `settings.json` are symlinks into the repo, so changes made in the app land directly in `home/.files/`.

## Layout

| Path                                | Purpose                                                                 |
| ----------------------------------- | ----------------------------------------------------------------------- |
| `home/`                             | chezmoi source directory (see `.chezmoiroot`)                           |
| `home/.chezmoi.toml.tmpl`           | Per-machine prompts                                                     |
| `home/.chezmoiexternal.toml.tmpl`   | Oh My Zsh, powerlevel10k and plugins, refreshed weekly                  |
| `home/.chezmoiignore`               | Per-OS ignores                                                          |
| `home/.chezmoidata/outside_home.yaml` | Files copied outside `$HOME` or to runtime paths (e.g. `$PROFILE`)    |
| `home/.files/`                      | Sources for symlinked and outside-`$HOME` files                         |
| `home/run_onchange_*`               | Package install and outside-`$HOME` deploy scripts                      |

To deploy another file outside `$HOME`, put it in `home/.files/` and add an entry to `outside_home.yaml`.

## Development

```bash
task test  # apply into a sandbox HOME (.sandbox/) without running scripts
```

CI applies the dotfiles on Ubuntu, macOS and Windows and checks that the shell starts without errors.
