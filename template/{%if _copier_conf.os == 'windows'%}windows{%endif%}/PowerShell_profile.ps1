## Environment Variables
$env:DEV = "D:\dev"
$env:UV_CACHE_DIR = "$env:DEV\.config\uv\cache"
$env:DOTFILES_PATH = "REPLACE_DOTFILES_PATH_HERE"
$env:STARSHIP_CONFIG = "$env:DEV\.config\starship\starship.toml"

## Allow terminating the shell with Ctrl+D
Set-PSReadlineKeyHandler -Chord Ctrl+d -Function DeleteCharOrExit

## starship theme
Invoke-Expression (&starship init powershell)

## uv shell completions - slow PowerShell startup
(& uv generate-shell-completion powershell) | Out-String | Invoke-Expression
(& uvx --generate-shell-completion powershell) | Out-String | Invoke-Expression

## git aliases
Import-Module git-aliases -DisableNameChecking

# dotfiles aliases
function GotoDotfiles {cd $env:DOTFILES_PATH}
function DotfilesUpdate {uvx copier update $env:DOTFILES_PATH --trust -A}
Set-Alias dotfiles GotoDotfiles
Set-Alias dotfiles-update DotfilesUpdate

# Python venv - activate local venv
function ActivateVenv {
    if ($env:UV_PROJECT_ENVIRONMENT) {
        . $env:UV_PROJECT_ENVIRONMENT/Scripts/Activate.ps1
    } else {
        . .venv/Scripts/Activate.ps1
    }
}
Set-Alias venv ActivateVenv
# Git alias to open current repository in browser
function open_github_repo {
    $repoUrl = git config --get remote.origin.url
    if ($repoUrl) {
        $webUrl = $repoUrl -replace 'git@github.com:', 'https://github.com/'
        Start-Process $webUrl
    } else {
        Write-Host "No Git repository found in current directory."
    }
}
Set-Alias gw OpenGithubRepo
