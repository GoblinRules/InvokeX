# InvokeX

A modern, user-friendly GUI application for installing popular Windows applications and applying system tweaks. Features a beautiful interface with real-time logging, auto-scaling, and comprehensive error handling.

## 🚀 Quick Install

### One-Line Installation (Recommended)
```powershell
irm https://raw.githubusercontent.com/GoblinRules/InvokeX/main/install.ps1 | iex
```

**That's it!** The installer automatically handles everything:
- ✅ **Python detection** and automatic installation
- ✅ **File downloads** from GitHub
- ✅ **Installation** to `C:\Tools\InvokeX`
- ✅ **Desktop shortcut** with custom icon
- ✅ **Start menu integration**

### 🖥️ Fix for Older Windows Systems (pre-TLS 1.2)

Run this first to enable TLS 1.2 and strong crypto:

```powershell
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
```
Then run:

```powershell
powershell -ExecutionPolicy Bypass -Command "irm https://raw.githubusercontent.com/GoblinRules/InvokeX/main/install.ps1 | iex"
```

### Manual Installation
1. Clone this repository
2. Ensure Python 3.6+ is installed
3. Run `python app_installer.py`

## ✨ Features

### 🎯 **Application Installation**
- **PyAutoClicker** - Automated clicking utility
- **IP Python Tray App** - System tray IP address display
- **PowerEventProvider** - Power management event provider
- **CTT WinUtil** - Windows utility collection
- **MASS** - Microsoft Activation Scripts

### 🔧 **System Tweaks**
- Remove shutdown option from startup power menu
- View power management event logs

### 🎨 **Modern UI**
- **Auto-scaling** - Responsive design that adapts to window resizing
- **Scrollable content** - Easy navigation through all options
- **Real-time terminal** - Live logging with color-coded messages
- **Status indicators** - Shows which apps are already installed
- **Professional styling** - Clean, modern interface

### 🛡️ **Smart Features**
- **Automatic Python detection** - Finds Python installations automatically
- **Automatic Python installation** - Installs Python if not found
- **Admin privilege management** - Detects and offers to restart with elevated rights
- **Comprehensive logging** - All operations logged to files and terminal
- **Error handling** - Graceful fallbacks and user-friendly error messages
- **Multiple installation methods** - Fallback options for failed installations

## 📋 Requirements

- **Windows 10/11**
- **Internet connection** (for downloads and installations)
- **Administrator privileges** (recommended for some operations)
- **Python 3.6+** (automatically installed if not found)

## 🚀 Installation Methods

### Method 1: PowerShell One-Liner (Easiest)
```powershell
irm https://raw.githubusercontent.com/GoblinRules/InvokeX/main/install.ps1 | iex
```

This will:
- ✅ **Automatically detect** if Python is installed
- ✅ **Install Python automatically** if needed (no manual intervention)
- ✅ **Download all application files** from GitHub
- ✅ **Install to `C:\Tools\InvokeX`**
- ✅ **Create desktop shortcut** with custom icon
- ✅ **Set up start menu integration**
- ✅ **Create uninstaller**

### Method 2: Manual Installation
```bash
# Clone the repository
git clone https://github.com/GoblinRules/InvokeX.git
cd InvokeX

# Install Python dependencies (if any)
pip install -r requirements.txt

# Run the application
python app_installer.py
```

### Method 3: Batch File
```batch
# Run the included batch file
run_installer.bat
```

## 🎮 Usage

### Starting the Application
1. **Desktop Shortcut** - Double-click the created `InvokeX.lnk` shortcut
2. **Start Menu** - Search for "InvokeX" in the Start Menu
3. **Command Line** - Run `python "C:\Tools\InvokeX\app_installer.py"`

### Installing Applications
1. Go to the **Apps** tab
2. Click the **Install** button for your desired application
3. Monitor progress in the terminal window
4. Check installation status indicators

### Applying System Tweaks
1. Go to the **Tweaks** tab
2. Click the **Apply** button for desired tweaks
3. Monitor progress in the terminal window

### Terminal Output
- **Green** - Information messages
- **Cyan** - Success messages
- **Yellow** - Warning messages
- **Red** - Error messages
- **Clear button** - Clears terminal output

## 🔧 Advanced Options

### PowerShell Installer Options
```powershell
# Show help
irm https://raw.githubusercontent.com/GoblinRules/InvokeX/main/install.ps1 | iex -Help

# Force reinstallation (if already installed)
irm https://raw.githubusercontent.com/GoblinRules/InvokeX/main/install.ps1 | iex -Force
```

### Manual Python Installation
If the automatic Python installer fails:
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Install with "Add to PATH" option checked
3. Restart your terminal/PowerShell
4. Run the installer again

## 📁 File Structure

```
C:\Tools\InvokeX\
├── app_installer.py      # Main GUI application
├── install.ps1           # PowerShell installer script
├── requirements.txt      # Python dependencies
├── run_installer.bat    # Windows batch file
├── README.md            # This file
├── icon.ico             # Custom application icon
├── uninstall.ps1        # Uninstaller script
└── logs/                # Application logs (created automatically)
```

## 🗑️ Uninstallation

### Using the Uninstaller
```powershell
powershell -ExecutionPolicy Bypass -File "C:\Tools\InvokeX\uninstall.ps1"
```

### Manual Uninstallation
1. Delete the `C:\Tools\InvokeX` directory
2. Remove desktop shortcut `InvokeX.lnk`
3. Remove start menu shortcuts from `%APPDATA%\Microsoft\Windows\Start Menu\Programs\InvokeX`

## 🐛 Troubleshooting

### Common Issues

#### Python Installation Fails
- The installer automatically attempts Python installation
- If it fails, check your internet connection and try again
- Ensure Windows Defender/antivirus isn't blocking downloads
- Try running as Administrator

#### Permission Errors
- Run as Administrator for best results
- The app will detect admin status and offer to restart with elevated privileges

#### Installation Failures
- Check the terminal output for detailed error messages
- Verify internet connection
- Ensure Windows Defender/antivirus isn't blocking downloads

#### MSI Installation Issues
- The app automatically handles MSI installation failures
- Offers manual installation options when automated methods fail
- Provides detailed error logging for troubleshooting

### Log Files
All operations are logged to timestamped files in the `logs/` directory:
- `invokex_YYYYMMDD_HHMMSS.log` - Application logs
- Terminal output shows real-time status

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **PyAutoClicker** - [GoblinRules](https://github.com/GoblinRules/PyAutoClicker)
- **IP Python Tray App** - [GoblinRules](https://github.com/GoblinRules/ippy-tray-app)
- **PowerEventProvider** - [GoblinRules](https://github.com/GoblinRules/powereventprovider)
- **CTT WinUtil** - [ChrisTitusTech](https://github.com/ChrisTitusTech/winutil)
- **MASS** - [massgravel](https://github.com/massgravel/Microsoft-Activation-Scripts)

## 📞 Support

- **Issues**: Create an issue on [GitHub](https://github.com/GoblinRules/InvokeX/issues)
- **Discussions**: Use GitHub Discussions for questions
- **Wiki**: Check the GitHub Wiki for detailed guides

---

**Made with ❤️ by [GoblinRules](https://github.com/GoblinRules) for the Windows community**

