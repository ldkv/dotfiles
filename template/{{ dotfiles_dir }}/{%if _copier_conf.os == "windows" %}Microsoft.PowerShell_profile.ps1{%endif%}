# Should be placed in $PROFILE
# Environment Variables
$env:DEV = "D:\dev"
$env:UV_CACHE_DIR = "$env:DEV\.config\uv\cache"
$env:STARSHIP_CONFIG = "$env:DEV\.config\starship\starship.tomleee"

# # Allow terminating the shell with Ctrl+D
Set-PSReadlineKeyHandler -Chord Ctrl+d -Function DeleteCharOrExit

# # uv shell completions - slow PowerShell startup
# (& uv generate-shell-completion powershell) | Out-String | Invoke-Expression
# (& uvx --generate-shell-completion powershell) | Out-String | Invoke-Expression

# # git aliases
Import-Module git-aliases -DisableNameChecking


# starship theme
Invoke-Expression (&starship init powershell)
