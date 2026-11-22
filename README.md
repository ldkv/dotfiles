# dotfiles

My dotfiles for Linux (apt), macOS and Windows, managed with [chezmoi](https://www.chezmoi.io/).

## What it sets up

- **Linux / macOS**: zsh as login shell, [Oh My Zsh](https://ohmyz.sh/), [powerlevel10k](https://github.com/romkatv/powerlevel10k), zsh-autosuggestions, fast-syntax-highlighting, `gh`, `task` and `uv`.
- **Windows**: PowerShell 7 profile with starship, git-aliases, `gh`, `task` (via [scoop](https://scoop.sh)) and `uv`.
- **Everywhere**: `.gitconfig`, `.taskrc.yml`, a `Taskfile.yml` in your dev folder, VS Code `settings.json`.

## Install

Always review before applying: `chezmoi apply` overwrites existing dotfiles, so local changes that are not in this repo are lost.

**1. Install chezmoi**

Linux / macOS:

```bash
sh -c "$(curl -fsLS get.chezmoi.io)" -- -b ~/.local/bin
export PATH="$HOME/.local/bin:$PATH"  # this session only, .zshrc adds it afterwards
```

Windows (PowerShell 7, [scoop](https://scoop.sh) installed, [Developer Mode](https://learn.microsoft.com/en-us/windows/apps/get-started/enable-your-device-for-development) enabled for symlinks):

```powershell
scoop install chezmoi
```

**2. Clone and answer the prompts** (nothing in `$HOME` changes yet)

```bash
chezmoi init ldkv/dotfiles
```

**3. Review what would change**

```bash
chezmoi status --exclude externals  # one line per file
chezmoi diff --exclude externals    # full diff
```

Bring anything you want to keep into the repo first (`chezmoi edit <file>`, or `chezmoi add <file>` for files not managed yet).

**4. Apply**

```bash
chezmoi apply
```

Then open a new shell and run `chezmoi verify`.

> [!NOTE]
> On a brand-new machine with no dotfiles to lose, steps 2–4 can be combined: `chezmoi init --apply ldkv/dotfiles`.

### Migrating from the old Copier setup (`~/.dotfiles`)

Before step 4:

1. Remove the old `Taskfile.yml` symlink (and `$PROFILE` on Windows): the deploy script copies through a symlink into `~/.dotfiles`, leaving a broken link once that folder is deleted. Other old symlinks (`.zshrc`, …) are replaced by `chezmoi apply` itself.

   ```bash
   find ~ -maxdepth 3 -type l -lname "$HOME/.dotfiles/*" -not -path "$HOME/.dotfiles/*" -exec ls -l {} \;  # list old symlinks
   f=~/dev/Taskfile.yml  # the Taskfile in your dev folder
   [ -L "$f" ] && rm -v "$f"
   ```

   ```powershell
   foreach ($f in $PROFILE, 'D:\dev\Taskfile.yml') {
       $item = Get-Item $f -ErrorAction SilentlyContinue
       if ($item.LinkType) { "$f -> $($item.Target)"; Remove-Item $f }
   }
   ```

2. Compare the old files with the new ones, since `chezmoi diff` only shows the symlinks being replaced:

   ```bash
   for f in .zshrc .zsh_aliases .gitconfig .taskrc.yml .p10k.zsh .uv_wrapper.zsh; do
     echo "== $f"; diff "$(readlink -f ~/$f)" <(chezmoi cat ~/$f)
   done
   ```

   Lines starting with `<` exist only in the old setup.

After step 4, delete `~/.dotfiles` once everything works.

`chezmoi init` asks once per machine:

| Prompt       | Used for                                   | Default                     |
| ------------ | ------------------------------------------ | --------------------------- |
| `user_name`  | git `user.name`                            | Vu LE                       |
| `user_email` | git `user.email`                           | ledkvu@gmail.com            |
| `dev_dir`    | where `Taskfile.yml` is copied, `$env:DEV` | `~/dev` (Windows: `D:\dev`) |
| `editor`     | git `core.editor`                          | `vim`                       |

WSL is detected automatically. To change an answer later, edit `~/.config/chezmoi/chezmoi.toml` (`chezmoi edit-config`).

## Daily use

Edit the source in the repo (`~/.local/share/chezmoi`), apply it to `$HOME`, push; other machines pull with `chezmoi update`.
Changes made through chezmoi are committed automatically, pushing is manual.

| I want to…                    | Run                                                                  |
| ----------------------------- | -------------------------------------------------------------------- |
| Edit a dotfile                | `chezmoi edit --apply ~/.zshrc`                                      |
| See pending changes           | `chezmoi diff` / `chezmoi status`                                    |
| Push my changes               | `chezmoi git push`                                                   |
| Pull and apply latest changes | `chezmoi update`                                                     |
| Bring back a local edit       | `chezmoi re-add` (plain files) / `chezmoi merge ~/.zshrc` (`.tmpl`)  |
| Track a new file              | `chezmoi add ~/.config/foo` (`--template` for per-OS/machine values) |
| Change a per-machine answer   | `chezmoi edit-config`, then `chezmoi apply`                          |
| Work in the repo              | `chezmoi cd`                                                         |

- **Edited `~/.zshrc` directly by mistake?** `chezmoi apply` detects it and asks before overwriting. `chezmoi re-add` skips templates (`.zshrc`, `.zsh_aliases`, `.gitconfig`, PowerShell profile), use `chezmoi merge` for those.
- **VS Code** `settings.json` is a symlink into `home/.files/`: change settings in the app, then commit from `chezmoi cd` (bypasses auto-commit).
- **Per-OS or per-machine differences**: template conditions (`{{ if eq .chezmoi.os "darwin" }}`) or prompt values (`.dev_dir`, `.editor`, `.is_wsl`); files for some OSes only go in `home/.chezmoiignore`.
- **Files outside `$HOME`**: put them in `home/.files/` and add an entry to `home/.chezmoidata/outside_home.yaml`.
- **Externals** (Oh My Zsh, powerlevel10k, plugins) refresh weekly on `chezmoi apply`; install scripts only rerun when their content changes.

## Layout

| Path                                  | Purpose                                                            |
| ------------------------------------- | ------------------------------------------------------------------ |
| `home/`                               | chezmoi source directory (see `.chezmoiroot`)                      |
| `home/.chezmoi.toml.tmpl`             | Per-machine prompts                                                |
| `home/.chezmoiexternal.toml.tmpl`     | Oh My Zsh, powerlevel10k and plugins, refreshed weekly             |
| `home/.chezmoiignore`                 | Per-OS ignores                                                     |
| `home/.chezmoidata/outside_home.yaml` | Files copied outside `$HOME` or to runtime paths (e.g. `$PROFILE`) |
| `home/.files/`                        | Sources for symlinked and outside-`$HOME` files                    |
| `home/run_onchange_*`                 | Package install script                                             |
| `home/run_after_*`                    | Outside-`$HOME` deploy scripts, run on every `chezmoi apply`       |

## Development

```bash
task test  # apply into a sandbox HOME (.sandbox/) without running scripts
```

CI applies the dotfiles on Ubuntu, macOS and Windows and checks that the shell starts without errors.
