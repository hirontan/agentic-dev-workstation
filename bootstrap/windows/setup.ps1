#Requires -Version 5.1
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [switch]$Apply,
    [ValidatePattern('^[A-Za-z0-9._-]+$')]
    [string]$Distro = 'Ubuntu-24.04'
)
$ErrorActionPreference = 'Stop'
Write-Host "Plan: set WSL default version to 2; install $Distro if absent."
Write-Host 'Existing distributions will not be converted, removed, or stopped.'
if (-not $Apply) {
    Write-Host 'No changes. Re-run with -Apply in an elevated PowerShell.'
    return
}
if (-not $PSCmdlet.ShouldProcess('Windows WSL', "Set default version and ensure $Distro")) {
    return
}
$identity = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object Security.Principal.WindowsPrincipal($identity)
if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    throw 'Open PowerShell as Administrator, then re-run with -Apply.'
}
function Invoke-WslChecked {
    param([string[]]$WslArguments)
    & wsl.exe @WslArguments
    if ($LASTEXITCODE -ne 0) {
        throw "WSL command failed (exit $LASTEXITCODE). Follow any restart instructions and retry."
    }
}
if (-not (Get-Command wsl.exe -ErrorAction SilentlyContinue)) {
    throw 'wsl.exe is unavailable. Install/update Windows WSL following Microsoft documentation.'
}
$raw = & wsl.exe --list --quiet 2>$null
$listExit = $LASTEXITCODE
$installed = @($raw | ForEach-Object { ($_ -replace "`0", '').Trim() } | Where-Object { $_ })
if ($listExit -ne 0) {
    # A fresh Windows installation may have wsl.exe but no enabled WSL components.
    Write-Host 'WSL list unavailable; starting Microsoft WSL installation.'
    Invoke-WslChecked -WslArguments @('--install', '-d', $Distro, '--no-launch')
    Write-Host 'If requested, restart Windows. Launch Ubuntu once to create a Linux user.'
    return
}
Invoke-WslChecked -WslArguments @('--set-default-version', '2')
if ($installed -contains $Distro) {
    Write-Host "$Distro already exists. Its existing version and user settings are preserved."
} else {
    Invoke-WslChecked -WslArguments @('--install', '-d', $Distro, '--no-launch')
}
Write-Host 'Verify wsl -l -v. Follow restart instructions, then launch Ubuntu and create a normal Linux user.'
