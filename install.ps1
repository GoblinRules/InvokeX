# ═══════════════════════════════════════════════════════════════
# InvokeX v2.0 — PowerShell Installer (Self-Contained)
# ═══════════════════════════════════════════════════════════════
# Usage: irm https://raw.githubusercontent.com/GoblinRules/InvokeX/main/install.ps1 | iex
#
# Downloads and installs the portable InvokeX.exe — no dependencies needed.
# ═══════════════════════════════════════════════════════════════

$ErrorActionPreference = "Stop"
$installDir = "C:\Tools\InvokeX"
$exeName = "InvokeX.exe"
$releaseUrl = "https://github.com/GoblinRules/InvokeX/releases/latest/download/InvokeX.exe"

function Write-Step { param($msg) Write-Host "`n[$((Get-Date).ToString('HH:mm:ss'))] $msg" -ForegroundColor Cyan }
function Write-OK   { param($msg) Write-Host "  ✓ $msg" -ForegroundColor Green }
function Write-Warn { param($msg) Write-Host "  ⚠ $msg" -ForegroundColor Yellow }
function Write-Err  { param($msg) Write-Host "  ✗ $msg" -ForegroundColor Red }

# ── Banner ──
Write-Host @"

  ╔══════════════════════════════════════╗
  ║        InvokeX v2.0 Installer       ║
  ║   Modern Windows Toolkit (Electron) ║
  ╚══════════════════════════════════════╝

"@ -ForegroundColor Magenta

# ── 1. Check Internet ──
Write-Step "Checking internet connectivity..."
try {
    $null = Invoke-WebRequest -Uri "https://www.google.com" -TimeoutSec 10 -UseBasicParsing -ErrorAction Stop
    Write-OK "Internet connection verified"
} catch {
    Write-Err "No internet connection detected. Please check your network and try again."
    exit 1
}

# ── 2. Create install directory ──
Write-Step "Preparing installation directory..."
if (-not (Test-Path "C:\Tools")) {
    New-Item -ItemType Directory -Path "C:\Tools" -Force | Out-Null
}
if (-not (Test-Path $installDir)) {
    New-Item -ItemType Directory -Path $installDir -Force | Out-Null
    Write-OK "Created: $installDir"
} else {
    Write-OK "Directory exists: $installDir"
}

# ── 3. Download InvokeX.exe ──
Write-Step "Downloading InvokeX.exe (~75MB)..."
$exePath = Join-Path $installDir $exeName

# Kill any running instance so we can overwrite the EXE
$running = Get-Process -Name "InvokeX" -ErrorAction SilentlyContinue
if ($running) {
    Write-Warn "InvokeX is currently running — closing it for update..."
    $running | Stop-Process -Force
    Start-Sleep -Seconds 2
}

try {
    Write-Host "  This may take a minute depending on your connection..." -ForegroundColor Yellow
    $tempDownload = "$env:TEMP\InvokeX_download.exe"
    Invoke-WebRequest -Uri $releaseUrl -OutFile $tempDownload -UseBasicParsing
    Move-Item $tempDownload $exePath -Force
    $fileSizeMB = [math]::Round((Get-Item $exePath).Length / 1MB, 1)
    Write-OK "Downloaded InvokeX.exe ($fileSizeMB MB)"
} catch {
    Write-Err "Failed to download InvokeX.exe: $($_.Exception.Message)"
    Write-Host "  Try downloading manually from: https://github.com/GoblinRules/InvokeX/releases" -ForegroundColor Yellow
    # Clean up temp file if it exists
    if (Test-Path "$env:TEMP\InvokeX_download.exe") { Remove-Item "$env:TEMP\InvokeX_download.exe" -Force -EA SilentlyContinue }
}

# ── 4. Download icon for shortcuts ──
$iconPath = Join-Path $installDir "icon.ico"
try {
    $iconUrl = "https://raw.githubusercontent.com/GoblinRules/InvokeX/main/assets/icon1.ico"
    Invoke-WebRequest -Uri $iconUrl -OutFile $iconPath -UseBasicParsing -ErrorAction Stop
} catch {
    Write-Warn "Could not download icon (shortcuts will use default icon)"
}

# ── 5. Create shortcuts ──
Write-Step "Creating shortcuts..."

# Desktop shortcut
try {
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $shortcutPath = Join-Path $desktopPath "InvokeX.lnk"
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($shortcutPath)
    $Shortcut.TargetPath = $exePath
    $Shortcut.WorkingDirectory = $installDir
    $Shortcut.Description = "InvokeX v2.0 — Modern Windows Toolkit"
    if (Test-Path $iconPath) { $Shortcut.IconLocation = $iconPath }
    $Shortcut.Save()
    Write-OK "Desktop shortcut created"
} catch {
    Write-Warn "Could not create desktop shortcut: $($_.Exception.Message)"
}

# Start menu shortcut
try {
    $startMenuDir = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\InvokeX"
    if (-not (Test-Path $startMenuDir)) { New-Item -ItemType Directory -Path $startMenuDir -Force | Out-Null }
    $startShortcut = Join-Path $startMenuDir "InvokeX.lnk"
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($startShortcut)
    $Shortcut.TargetPath = $exePath
    $Shortcut.WorkingDirectory = $installDir
    $Shortcut.Description = "InvokeX v2.0 — Modern Windows Toolkit"
    if (Test-Path $iconPath) { $Shortcut.IconLocation = $iconPath }
    $Shortcut.Save()
    Write-OK "Start menu shortcut created"
} catch {
    Write-Warn "Could not create start menu shortcut: $($_.Exception.Message)"
}

# ── 6. Done ──
Write-Step "Installation complete!"
Write-Host @"

  ╔══════════════════════════════════════╗
  ║     InvokeX v2.0 installed!         ║
  ║                                     ║
  ║  Location: C:\Tools\InvokeX         ║
  ║  Shortcut: Desktop & Start Menu     ║
  ║                                     ║
  ║  Self-contained — no dependencies!  ║
  ║                                     ║
  ║  To update: Re-run this command     ║
  ║  To remove: Run uninstall.ps1       ║
  ╚══════════════════════════════════════╝

"@ -ForegroundColor Green

$launch = Read-Host "Launch InvokeX now? (Y/n)"
if ($launch -ne 'n' -and $launch -ne 'N') {
    Write-Host "  Starting InvokeX..." -ForegroundColor Cyan
    Start-Process -FilePath $exePath -WorkingDirectory $installDir
}
