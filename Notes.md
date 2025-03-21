Setup guide step by step for a new Ubuntu server 24.04 LTS

# First time setup

## Install [Oh My Zsh](https://ohmyz.sh/)

### Install base

```bash
sudo apt-get install zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

### Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install copier as uv tool

```bash
uv tool install copier
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

### Install postgresql DB

```bash
brew install postgresql@17
echo 'export PATH="/opt/homebrew/opt/postgresql@17/bin:$PATH"' >> ~/.zshrc
brew services start postgresql@17
```

Commands to generate user + password + DB:

```bash
psql postgres
CREATE USER postgres WITH SUPERUSER PASSWORD 'postgres';
CREATE DATABASE db1 WITH OWNER postgres;
CREATE DATABASE db2 WITH OWNER postgres;
```

## Github CLI & Git configuration

### Install Github CLI

https://github.com/cli/cli#installation

### Configure Git

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

## SSH to WSL2

<!-- https://medium.com/@wuzhenquan/windows-and-wsl-2-setup-for-ssh-remote-access-013955b2f421 -->

<!-- Use tailscale instead!!! https://tailscale.com/ -->

In WSL2:

```bash
sudo apt remove openssh-server
sudo apt install openssh-server
sudo vi /etc/ssh/sshd_config, enable Port 22 and PasswordAuthentication yes
sudo service ssh restart
```

Open Powershell in administrator mode.

Port forwarding:

```shell
netsh interface portproxy add v4tov4 `
  listenaddress=192.168.1.12 `
  listenport=2222 `
  connectaddress=172.18.95.67 `
  connectport=22
```

`listenaddress` is the IP address of the Windows host, `connectaddress` is the IP address of the WSL2 VM.

Add firewall rule:

```shell
netsh advfirewall firewall add rule `
name = "Allow Inbound 2222 WSL2 ssh" `
dir=in `
protocol=TCP `
localport=2222 `
action=allow
```

Finally:

```bash
ssh ldkv@192.168.1.12 -p 2222
```

If not working, reset port proxy (then retry commands above):

```shell
netsh interface portproxy reset
```

## Install OMZ plugins

```bash
#!/bin/sh

# Install zsh if not already installed
if ! command -v zsh >/dev/null 2>&1; then
    sudo apt update
    sudo apt install -y zsh
else
    echo "zsh is already installed"
fi

# Install oh-my-zsh if not already installed
if [ ! -d "$HOME/.oh-my-zsh" ]; then
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
else
    echo "oh-my-zsh is already installed"
fi

# Install oh-my-zsh plugins if not already installed
if [ ! -d "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-autosuggestions" ]; then
    git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
else
    echo "zsh-autosuggestions plugin is already installed"
fi

if [ ! -d "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/fast-syntax-highlighting" ]; then
    git clone https://github.com/zdharma-continuum/fast-syntax-highlighting.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/fast-syntax-highlighting
else
    echo "fast-syntax-highlighting plugin is already installed"
fi

if [ ! -d "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/ohmyzsh-full-autoupdate" ]; then
    git clone https://github.com/Pilaton/OhMyZsh-full-autoupdate.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/ohmyzsh-full-autoupdate
else
    echo "ohmyzsh-full-autoupdate plugin is already installed"
fi

# Install powerlevel10k theme
if [ ! -d "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k" ]; then
    git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
else
    echo "powerlevel10k theme is already installed"
fi
```

## Git bare repository

# Reference

https://www.atlassian.com/git/tutorials/dotfiles

# Steps

```bash
git init --bare $HOME/.dotfiles
alias dot='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
dot config --local status.showUntrackedFiles no
```

Add the following to `.gitignore`:

```bash
echo ".dotfiles" >> $HOME/.gitignore
```

Add the tracked files:

```bash
dot add $HOME/.zshrc
dot add $HOME/.gitconfig
dot add $HOME/.p10k.zsh
dot add $HOME/.gitignore
dot commit -m "Init with dotfiles"
```
