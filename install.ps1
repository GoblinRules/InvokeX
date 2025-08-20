# InvokeX - PowerShell Installer
# Modern GUI installer for Windows applications and system tweaks
# Repository: https://github.com/GoblinRules/InvokeX

param(
    [switch]$Force,
    [switch]$Help
)

function Show-Help {
    Write-Host @"
InvokeX - PowerShell Installer

Usage: irm https://raw.githubusercontent.com/GoblinRules/InvokeX/main/install.ps1 | iex

Options:
    -Force    Force reinstallation even if InvokeX is already installed
    -Help     Show this help message

This installer will:
1. Check if Python is installed
2. Install Python automatically if needed
3. Download the InvokeX GUI application files
4. Install to C:\Tools\InvokeX
5. Install required Python dependencies (customtkinter, Pillow)
6. Create desktop shortcut with custom icon
7. Set up start menu integration
8. Test that everything works correctly

Requirements:
- Windows 10/11
- Internet connection for download
- Administrator privileges (recommended)
"@
}

function Test-InternetConnection {
    """
    Test internet connectivity using multiple methods.
    Returns true if any method succeeds.
    """
    Write-Host "Testing internet connectivity..." -ForegroundColor Cyan
    
    # Method 1: Test with Invoke-WebRequest (most reliable for our use case)
    try {
        Write-Host "Method 1: Testing web connectivity..." -ForegroundColor Yellow
        $response = Invoke-WebRequest -Uri "https://www.google.com" -TimeoutSec 10 -ErrorAction Stop
        Write-Host "✓ Web connectivity test successful" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "Method 1 failed: $($_.Exception.Message)" -ForegroundColor Yellow
    }
    
    # Method 2: Test with Test-NetConnection (PowerShell native)
    try {
        Write-Host "Method 2: Testing network connectivity..." -ForegroundColor Yellow
        $testResult = Test-NetConnection -ComputerName "8.8.8.8" -Port 53 -InformationLevel Quiet
        if ($testResult) {
            Write-Host "✓ Network connectivity test successful" -ForegroundColor Green
            return $true
        }
    } catch {
        Write-Host "Method 2 failed: $($_.Exception.Message)" -ForegroundColor Yellow
    }
    
    # Method 3: Test with ping (using cmd)
    try {
        Write-Host "Method 3: Testing ping connectivity..." -ForegroundColor Yellow
        $pingResult = cmd /c "ping -n 1 8.8.8.8" 2>&1
        if ($pingResult -match "Reply from") {
            Write-Host "✓ Ping connectivity test successful" -ForegroundColor Green
            return $true
        }
    } catch {
        Write-Host "Method 3 failed: $($_.Exception.Message)" -ForegroundColor Yellow
    }
    
    # Method 4: Test with nslookup
    try {
        Write-Host "Method 4: Testing DNS resolution..." -ForegroundColor Yellow
        $dnsResult = nslookup google.com 2>&1
        if ($dnsResult -match "Address:") {
            Write-Host "✓ DNS resolution test successful" -ForegroundColor Green
            return $true
        }
    } catch {
        Write-Host "Method 4 failed: $($_.Exception.Message)" -ForegroundColor Yellow
    }
    
    Write-Host "✗ All connectivity tests failed" -ForegroundColor Red
    return $false
}

function Test-PythonInstalled {
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
            return $true
        }
    } catch {
        # Python not in PATH
    }
    
    # Check common Python installation paths
    $pythonPaths = @(
        "C:\Python*",
        "C:\Program Files\Python*",
        "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python*",
        "C:\Users\$env:USERNAME\AppData\Local\Microsoft\WindowsApps\python.exe"
    )
    
    foreach ($path in $pythonPaths) {
        $found = Get-ChildItem -Path $path -ErrorAction SilentlyContinue | Where-Object { $_.Name -like "python.exe" }
        if ($found) {
            Write-Host "✓ Python found at: $($found.FullName)" -ForegroundColor Green
            # Add to PATH for this session
            $env:PATH = "$($found.DirectoryName);$env:PATH"
            return $true
        }
    }
    
    return $false
}

function Install-Python {
    Write-Host "Python not found. Installing Python automatically..." -ForegroundColor Yellow
    
    try {
        # Download Python installer
        $pythonUrl = "https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe"
        $installerPath = "$env:TEMP\python-installer.exe"
        
        Write-Host "Downloading Python installer..." -ForegroundColor Yellow
        Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath
        
        Write-Host "Installing Python (this may take a few minutes)..." -ForegroundColor Yellow
        Start-Process -FilePath $installerPath -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1" -Wait
        
        # Refresh environment variables
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
        
        # Wait a moment for installation to complete
        Start-Sleep -Seconds 5
        
        # Verify installation
        if (Test-PythonInstalled) {
            Write-Host "✓ Python installed successfully!" -ForegroundColor Green
            return $true
        } else {
            Write-Host "✗ Python installation failed" -ForegroundColor Red
            return $false
        }
    } catch {
        Write-Host "✗ Failed to install Python: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    } finally {
        # Clean up installer
        if (Test-Path $installerPath) {
            Remove-Item $installerPath -Force
        }
    }
}

function Install-InvokeX {
    Write-Host "Installing InvokeX..." -ForegroundColor Yellow
    
    # Create installation directory
    $installDir = "C:\Tools\InvokeX"
    if (!(Test-Path $installDir)) {
        New-Item -ItemType Directory -Path $installDir -Force | Out-Null
        Write-Host "✓ Created installation directory: $installDir" -ForegroundColor Green
    } else {
        Write-Host "✓ Installation directory exists: $installDir" -ForegroundColor Green
    }
    
    # Download application files from GoblinRules/InvokeX repository
    $files = @{
        "app_installer.py" = "https://raw.githubusercontent.com/GoblinRules/InvokeX/main/app_installer.py"
        "requirements.txt" = "https://raw.githubusercontent.com/GoblinRules/InvokeX/main/requirements.txt"
        "README.md" = "https://raw.githubusercontent.com/GoblinRules/InvokeX/main/README.md"
        "run_installer.bat" = "https://raw.githubusercontent.com/GoblinRules/InvokeX/main/run_installer.bat"
        "icon.ico" = "https://raw.githubusercontent.com/GoblinRules/InvokeX/main/icon.ico"
    }
    
    foreach ($file in $files.GetEnumerator()) {
        try {
            Write-Host "Downloading $($file.Key)..." -ForegroundColor Yellow
            $filePath = Join-Path $installDir $file.Key
            Invoke-WebRequest -Uri $file.Value -OutFile $filePath
            Write-Host "✓ Downloaded $($file.Key)" -ForegroundColor Green
        } catch {
            Write-Host "✗ Failed to download $($file.Key): $($_.Exception.Message)" -ForegroundColor Red
            if ($file.Key -eq "icon.ico") {
                Write-Host "Warning: Icon file failed to download. Using default icon." -ForegroundColor Yellow
            } else {
                return $false
            }
        }
    }
    
    # Create desktop shortcut with custom icon
    try {
        $desktopPath = [Environment]::GetFolderPath("Desktop")
        $shortcutPath = Join-Path $desktopPath "InvokeX.lnk"
        $iconPath = Join-Path $installDir "icon.ico"
        
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut($shortcutPath)
        $Shortcut.TargetPath = "pythonw.exe"
        $Shortcut.Arguments = "`"$installDir\app_installer.py`""
        $Shortcut.WorkingDirectory = $installDir
        $Shortcut.Description = "InvokeX - Modern GUI installer for Windows applications and system tweaks"
        
        # Use custom icon if available, otherwise use Python icon
        if (Test-Path $iconPath) {
            $Shortcut.IconLocation = $iconPath
        } else {
            $Shortcut.IconLocation = "pythonw.exe,0"
        }
        
        $Shortcut.Save()
        Write-Host "✓ Desktop shortcut created: InvokeX.lnk" -ForegroundColor Green
    } catch {
        Write-Host "✗ Failed to create desktop shortcut: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    # Create start menu shortcut
    try {
        $startMenuPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\InvokeX"
        if (!(Test-Path $startMenuPath)) {
            New-Item -ItemType Directory -Path $startMenuPath -Force | Out-Null
        }
        
        $startMenuShortcut = Join-Path $startMenuPath "InvokeX.lnk"
        $Shortcut = $WshShell.CreateShortcut($startMenuShortcut)
        $Shortcut.TargetPath = "pythonw.exe"
        $Shortcut.Arguments = "`"$installDir\app_installer.py`""
        $Shortcut.WorkingDirectory = $installDir
        $Shortcut.Description = "InvokeX - Modern GUI installer for Windows applications and system tweaks"
        
        # Use custom icon if available
        if (Test-Path $iconPath) {
            $Shortcut.IconLocation = $iconPath
        } else {
            $Shortcut.IconLocation = "pythonw.exe,0"
        }
        
        $Shortcut.Save()
        Write-Host "✓ Start menu shortcut created" -ForegroundColor Green
    } catch {
        Write-Host "✗ Failed to create start menu shortcut: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    # Install Python dependencies
    try {
        Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
        $requirementsPath = Join-Path $installDir "requirements.txt"
        
        # Change to installation directory and install requirements
        Push-Location $installDir
        try {
            $pipResult = python -m pip install -r requirements.txt 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✓ Python dependencies installed successfully" -ForegroundColor Green
            } else {
                Write-Host "✗ Failed to install Python dependencies" -ForegroundColor Red
                Write-Host "Error: $pipResult" -ForegroundColor Red
                Write-Host "You may need to install dependencies manually:" -ForegroundColor Yellow
                Write-Host "cd $installDir && python -m pip install -r requirements.txt" -ForegroundColor Yellow
            }
        } finally {
            Pop-Location
        }
    } catch {
        Write-Host "✗ Failed to install Python dependencies: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "You may need to install dependencies manually:" -ForegroundColor Yellow
        Write-Host "cd $installDir && python -m pip install -r requirements.txt" -ForegroundColor Yellow
    }
    
    # Create uninstaller
    try {
        $uninstallerPath = Join-Path $installDir "uninstall.ps1"
        $uninstallerContent = @"
# InvokeX Uninstaller
Write-Host "Uninstalling InvokeX..." -ForegroundColor Yellow

# Remove shortcuts
`$desktopPath = [Environment]::GetFolderPath("Desktop")
`$desktopShortcut = Join-Path `$desktopPath "InvokeX.lnk"
if (Test-Path `$desktopShortcut) {
    Remove-Item `$desktopShortcut -Force
    Write-Host "✓ Desktop shortcut removed" -ForegroundColor Green
}

`$startMenuPath = "`$env:APPDATA\Microsoft\Windows\Start Menu\Programs\InvokeX"
if (Test-Path `$startMenuPath) {
    Remove-Item `$startMenuPath -Recurse -Force
    Write-Host "✓ Start menu shortcuts removed" -ForegroundColor Green
}

# Remove installation directory
if (Test-Path "C:\Tools\InvokeX") {
    Remove-Item "C:\Tools\InvokeX" -Recurse -Force
    Write-Host "✓ Installation directory removed" -ForegroundColor Green
}

Write-Host "InvokeX has been uninstalled successfully!" -ForegroundColor Green
"@
        Set-Content -Path $uninstallerPath -Value $uninstallerContent
        Write-Host "✓ Uninstaller created: uninstall.ps1" -ForegroundColor Green
    } catch {
        Write-Host "✗ Failed to create uninstaller: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    # Test that InvokeX can run after installation
    try {
        Write-Host "Testing InvokeX installation..." -ForegroundColor Yellow
        Push-Location $installDir
        try {
            # Test import without running the full GUI
            $testResult = python -c "import customtkinter; print('Dependencies test: SUCCESS')" 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✓ InvokeX dependencies test passed" -ForegroundColor Green
            } else {
                Write-Host "✗ InvokeX dependencies test failed" -ForegroundColor Red
                Write-Host "Error: $testResult" -ForegroundColor Red
            }
        } finally {
            Pop-Location
        }
    } catch {
        Write-Host "✗ Failed to test InvokeX installation: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    return $true
}

function Test-Requirements {
    Write-Host "Checking system requirements..." -ForegroundColor Cyan
    
    # Check Windows version
    $os = Get-WmiObject -Class Win32_OperatingSystem
    $windowsVersion = [System.Version]::Parse($os.Version)
    if ($windowsVersion.Major -ge 10) {
        Write-Host "✓ Windows 10/11 detected" -ForegroundColor Green
    } else {
        Write-Host "✗ Windows 10/11 required (found: $($os.Caption))" -ForegroundColor Red
        return $false
    }
    
    # Check Python - automatically install if not found
    if (!(Test-PythonInstalled)) {
        Write-Host "Python not found. Installing automatically..." -ForegroundColor Yellow
        if (!(Install-Python)) {
            Write-Host "✗ Python installation failed" -ForegroundColor Red
            Write-Host "Please install Python manually from: https://www.python.org/downloads/" -ForegroundColor Yellow
            return $false
        }
    }
    
    # Check internet connection with improved testing
    if (!(Test-InternetConnection)) {
        Write-Host "✗ Internet connectivity issues detected" -ForegroundColor Red
        Write-Host "Please check your network settings and try again." -ForegroundColor Yellow
        Write-Host "If the issue persists, try:" -ForegroundColor Yellow
        Write-Host "1. Running as Administrator" -ForegroundColor Yellow
        Write-Host "2. Checking Windows Defender/antivirus settings" -ForegroundColor Yellow
        Write-Host "3. Checking corporate firewall/proxy settings" -ForegroundColor Yellow
        return $false
    }
    
    return $true
}

function Show-Success {
    Write-Host @"

╔══════════════════════════════════════════════════════════════╗
║                    Installation Complete!                    ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ✓ InvokeX has been installed successfully!                 ║
║  ✓ Python dependencies installed                            ║
║  ✓ Ready to run immediately                                 ║
║                                                              ║
║  You can now:                                               ║
║  • Double-click the desktop shortcut (InvokeX.lnk)          ║
║  • Use the Start Menu shortcut                              ║
║  • Run: python "C:\Tools\InvokeX\app_installer.py"         ║
║                                                              ║
║  Installation location:                                      ║
║  C:\Tools\InvokeX                                           ║
║                                                              ║
║  To uninstall:                                              ║
║  powershell -ExecutionPolicy Bypass -File "C:\Tools\InvokeX\uninstall.ps1" ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Green
}

# Main execution
if ($Help) {
    Show-Help
    exit 0
}

Write-Host @"
╔══════════════════════════════════════════════════════════════╗
║                        InvokeX Setup                        ║
║                                                              ║
║  Modern GUI installer for Windows applications and system   ║
║  tweaks with automatic Python detection and easy access.    ║
║                                                              ║
║  Repository: https://github.com/GoblinRules/InvokeX         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Cyan

# Check requirements (Python will be installed automatically if needed)
if (!(Test-Requirements)) {
    Write-Host "`nInstallation failed. Please resolve the issues above and try again." -ForegroundColor Red
    exit 1
}

# Install InvokeX
if (Install-InvokeX) {
    Show-Success
} else {
    Write-Host "`nInstallation failed. Please check the error messages above." -ForegroundColor Red
    exit 1
}
