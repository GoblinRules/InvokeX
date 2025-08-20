# InvokeX Uninstaller
Write-Host "Uninstalling InvokeX..." -ForegroundColor Yellow

# Remove shortcuts
$desktopPath = [Environment]::GetFolderPath("Desktop")
$desktopShortcut = Join-Path $desktopPath "InvokeX.lnk"
if (Test-Path $desktopShortcut) {
    Remove-Item $desktopShortcut -Force
    Write-Host "? Desktop shortcut removed" -ForegroundColor Green
}

$startMenuPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\InvokeX"
if (Test-Path $startMenuPath) {
    Remove-Item $startMenuPath -Recurse -Force
    Write-Host "? Start menu shortcuts removed" -ForegroundColor Green
}

# Remove installation directory
if (Test-Path "C:\Tools\InvokeX") {
    Remove-Item "C:\Tools\InvokeX" -Recurse -Force
    Write-Host "? Installation directory removed" -ForegroundColor Green
}

Write-Host "InvokeX has been uninstalled successfully!" -ForegroundColor Green
