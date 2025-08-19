# InvokeX - Application & Tweak Installer

A modern GUI installer for Windows applications and system tweaks.

## Quick Start

### Run the Application
- **Recommended**: Double-click `InvokeX.pyw` (runs without console window)
- **Alternative**: Run `python app_installer.py`

### Requirements
- Windows 10/11
- Python 3.7+
- Administrator privileges (recommended)

## Features

### Applications
- PyAutoClicker - Automated clicking utility
- IP Python Tray App - System tray IP address display  
- PowerEventProvider - Power management event provider
- CTT WinUtil - Windows utility collection
- MASS - Microsoft Activation Scripts
- Tailscale - VPN and secure networking
- MuMu - Android emulator for Windows
- Ninite Installer - Essential apps (7zip, Chrome, Firefox, Notepad++)

### System Tweaks
- Hide Shutdown Options - Hide shutdown/sleep/hibernate from start menu
- Set Chrome As Default Browser - Configure Chrome as default browser
- Power Management Settings - Never sleep/hibernate, disable power button
- User Account Management - Prevent user creation, create admin accounts
- Remote Desktop - Enable/disable RDP connections

## Files Structure

- `app_installer.py` - Main application file
- `InvokeX.pyw` - Clean execution file (no console)
- `icon.ico` - Application icon
- `install.ps1` - PowerShell installer
- `run_installer.bat` - Batch installer
- `backup_files/` - Old versions and backups
- `development/` - Development utilities
- `logs/` - Application logs

## Usage Notes

- Run as administrator for full functionality
- All downloads and installations are logged to the terminal
- Status indicators show installation/activation status for each app
- Power management changes take effect immediately
- System tweaks use Group Policy Objects (GPO) for reliability

## Version
Current Version: 1.0.0