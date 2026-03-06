# ═══════════════════════════════════════════════════════════════
# InvokeX v2.0 — PowerShell Installer
# ═══════════════════════════════════════════════════════════════
# Usage: irm https://raw.githubusercontent.com/GoblinRules/InvokeX/main/install.ps1 | iex
#
# This installer will:
# 1. Check/install Node.js if needed
# 2. Clone or download InvokeX from GitHub
# 3. Install npm dependencies
# 4. Create desktop & start menu shortcuts
# 5. Launch InvokeX
# ═══════════════════════════════════════════════════════════════

$ErrorActionPreference = "Stop"
$installDir = "C:\Tools\InvokeX"
$repoUrl = "https://github.com/GoblinRules/InvokeX.git"
$repoZip = "https://github.com/GoblinRules/InvokeX/archive/refs/heads/main.zip"

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

# ── 2. Check/Install Node.js ──
Write-Step "Checking for Node.js..."
$nodeInstalled = $false
try {
    $nodeVersion = node --version 2>$null
    if ($LASTEXITCODE -eq 0 -and $nodeVersion) {
        Write-OK "Node.js found: $nodeVersion"
        $nodeInstalled = $true
    }
} catch {}

if (-not $nodeInstalled) {
    Write-Warn "Node.js not found. Installing Node.js LTS..."
    try {
        # Download Node.js LTS installer
        $nodeUrl = "https://nodejs.org/dist/v20.11.1/node-v20.11.1-x64.msi"
        $nodeInstaller = "$env:TEMP\node-installer.msi"
        Write-Host "  Downloading Node.js LTS..." -ForegroundColor Yellow
        Invoke-WebRequest -Uri $nodeUrl -OutFile $nodeInstaller -UseBasicParsing
        Write-Host "  Installing Node.js (this may take a minute)..." -ForegroundColor Yellow
        Start-Process msiexec.exe -ArgumentList "/i", "`"$nodeInstaller`"", "/qn", "/norestart" -Wait
        # Refresh PATH
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
        Start-Sleep -Seconds 3
        $nodeVersion = node --version 2>$null
        if ($nodeVersion) {
            Write-OK "Node.js installed: $nodeVersion"
        } else {
            Write-Err "Node.js installation completed but 'node' not found in PATH."
            Write-Warn "Please restart your terminal and run this installer again."
            exit 1
        }
        Remove-Item $nodeInstaller -Force -ErrorAction SilentlyContinue
    } catch {
        Write-Err "Failed to install Node.js: $($_.Exception.Message)"
        Write-Warn "Please install Node.js manually from https://nodejs.org and run this installer again."
        exit 1
    }
}

# ── 3. Download InvokeX ──
Write-Step "Downloading InvokeX..."

# Check if git is available
$hasGit = $false
try {
    $null = git --version 2>$null
    if ($LASTEXITCODE -eq 0) { $hasGit = $true }
} catch {}

if (Test-Path $installDir) {
    if (Test-Path "$installDir\.git") {
        Write-Host "  Existing installation found. Pulling latest updates..." -ForegroundColor Yellow
        Push-Location $installDir
        git pull origin main 2>$null
        Pop-Location
        Write-OK "Updated to latest version"
    } else {
        Write-Host "  Existing installation found (no git). Backing up and re-downloading..." -ForegroundColor Yellow
        $backupDir = "${installDir}_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        Rename-Item $installDir $backupDir
        Write-OK "Backup created: $backupDir"
    }
}

if (-not (Test-Path $installDir)) {
    if ($hasGit) {
        Write-Host "  Cloning repository..." -ForegroundColor Yellow
        git clone $repoUrl $installDir 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Err "Git clone failed. Falling back to ZIP download..."
            $hasGit = $false
        } else {
            Write-OK "Repository cloned successfully"
        }
    }

    if (-not $hasGit -or -not (Test-Path $installDir)) {
        Write-Host "  Downloading ZIP archive..." -ForegroundColor Yellow
        $zipPath = "$env:TEMP\InvokeX.zip"
        Invoke-WebRequest -Uri $repoZip -OutFile $zipPath -UseBasicParsing
        Expand-Archive -Path $zipPath -DestinationPath "$env:TEMP\InvokeX-extract" -Force
        # Move extracted folder to install dir
        $extractedDir = Get-ChildItem "$env:TEMP\InvokeX-extract" | Select-Object -First 1
        if (-not (Test-Path "C:\Tools")) { New-Item -ItemType Directory -Path "C:\Tools" -Force | Out-Null }
        Move-Item $extractedDir.FullName $installDir -Force
        Remove-Item $zipPath -Force -ErrorAction SilentlyContinue
        Remove-Item "$env:TEMP\InvokeX-extract" -Recurse -Force -ErrorAction SilentlyContinue
        Write-OK "Downloaded and extracted successfully"
    }
}

# ── 4. Install npm dependencies ──
Write-Step "Installing dependencies..."
Push-Location $installDir
try {
    npm install --production 2>&1 | Out-Null
    Write-OK "Dependencies installed"
} catch {
    Write-Err "npm install failed: $($_.Exception.Message)"
    Pop-Location
    exit 1
}
Pop-Location

# ── 5. Create shortcuts ──
Write-Step "Creating shortcuts..."

# Find electron.exe
$electronExe = Join-Path $installDir "node_modules\electron\dist\electron.exe"
$iconPath = Join-Path $installDir "assets\icon1.ico"

# Desktop shortcut
try {
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $shortcutPath = Join-Path $desktopPath "InvokeX.lnk"
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($shortcutPath)
    $Shortcut.TargetPath = $electronExe
    $Shortcut.Arguments = "."
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
    $startMenuPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\InvokeX"
    if (-not (Test-Path $startMenuPath)) { New-Item -ItemType Directory -Path $startMenuPath -Force | Out-Null }
    $startShortcut = Join-Path $startMenuPath "InvokeX.lnk"
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($startShortcut)
    $Shortcut.TargetPath = $electronExe
    $Shortcut.Arguments = "."
    $Shortcut.WorkingDirectory = $installDir
    $Shortcut.Description = "InvokeX v2.0 — Modern Windows Toolkit"
    if (Test-Path $iconPath) { $Shortcut.IconLocation = $iconPath }
    $Shortcut.Save()
    Write-OK "Start menu shortcut created"
} catch {
    Write-Warn "Could not create start menu shortcut: $($_.Exception.Message)"
}

# ── 6. Launch InvokeX ──
Write-Step "Installation complete!"
Write-Host @"

  ╔══════════════════════════════════════╗
  ║     InvokeX v2.0 installed!         ║
  ║                                     ║
  ║  Location: C:\Tools\InvokeX         ║
  ║  Shortcut: Desktop & Start Menu     ║
  ║                                     ║
  ║  To run:   Double-click shortcut    ║
  ║     or:    cd C:\Tools\InvokeX      ║
  ║            npm run dev              ║
  ║                                     ║
  ║  To update: Re-run this command     ║
  ║  To remove: Run uninstall.ps1       ║
  ╚══════════════════════════════════════╝

"@ -ForegroundColor Green

$launch = Read-Host "Launch InvokeX now? (Y/n)"
if ($launch -ne 'n' -and $launch -ne 'N') {
    Write-Host "  Starting InvokeX..." -ForegroundColor Cyan
    Start-Process -FilePath $electronExe -ArgumentList "." -WorkingDirectory $installDir
}
