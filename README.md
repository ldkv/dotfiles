Setup guide step by step for a new Ubuntu server 24.04 LTS

# First time setup

## Install [Oh My Zsh](https://ohmyz.sh/)

### Install base

```bash
sudo apt-get install zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

### Install plugins

- [git](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/git): provides aliases and functions for git commands
- [gh](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/gh): adds completion for GitHub CLI
- [z](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/z): tracks most used directories and allows to jump to them
- [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions/): suggests commands based on history
- [fast-syntax-highlighting](https://github.com/zdharma-continuum/fast-syntax-highlighting): highlights commands while typing
- [ohmyzsh-full-autoupdate](https://github.com/Pilaton/OhMyZsh-full-autoupdate): updates Oh My Zsh custom plugins and themes automatically

Execute commands:

```bash
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
git clone https://github.com/zdharma-continuum/fast-syntax-highlighting.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/fast-syntax-highlighting
git clone https://github.com/Pilaton/OhMyZsh-full-autoupdate.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/ohmyzsh-full-autoupdate
```

Add to `~/.zshrc` plugins list:

```bash
plugins=(
    ...
    git
    gh
    z
    zsh-autosuggestions
    fast-syntax-highlighting
    ohmyzsh-full-autoupdate
)

```

### Install theme [powerlevel10k](https://github.com/romkatv/powerlevel10k)

- Install as a regular Oh My Zsh theme:

```bash
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
```

- Set `ZSH_THEME="powerlevel10k/powerlevel10k"` in `~/.zshrc`.
- Run `p10k configure` to configure the theme.
- A preconfigured `.p10k.zsh` file is available in this repository.

## Install [brew](https://brew.sh/)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Install packages

```bash
brew install gh
brew install pyenv
```

## Configure Git

```bash
git config --global user.name "Vu LE"
git config --global user.email "ledkvu@gmail.com"
```

## Install [Docker](https://docs.docker.com/engine/install/ubuntu/)

- Install prerequisites:

```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

- Install Docker:

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

- Enable user to run Docker commands without `sudo`:

```bash
sudo groupadd docker
sudo usermod -aG docker $USER
sudo systemctl restart docker
```
