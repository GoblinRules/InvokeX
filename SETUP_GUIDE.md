# 🚀 InvokeX GitHub Repository Setup Guide

This guide will help you set up your [InvokeX repository](https://github.com/GoblinRules/InvokeX) with all the necessary files and configurations.

## 📋 **Repository Setup Steps**

### 1. **Clone and Prepare Your Repository**
```bash
git clone https://github.com/GoblinRules/InvokeX.git
cd InvokeX
```

### 2. **Upload All Files**
Upload these files to your repository root:

#### **Core Application Files:**
- ✅ `app_installer.py` - Main GUI application (fully annotated)
- ✅ `install.ps1` - PowerShell installer script
- ✅ `requirements.txt` - Python dependencies
- ✅ `run_installer.bat` - Windows batch file
- ✅ `README.md` - Comprehensive documentation
- ✅ `create_icon.py` - Icon generator script

#### **GitHub Configuration Files:**
- ✅ `.github/workflows/test-installer.yml` - GitHub Actions testing
- ✅ `.github/ISSUE_TEMPLATE/bug_report.md` - Issue template

### 3. **Generate the Icon**
```bash
# Install Pillow if needed
pip install Pillow

# Generate the InvokeX icon
python create_icon.py
```

This will create `icon.ico` - a modern, tech-inspired icon with:
- Dark background (#1E1E1E)
- Blue accent (#0096FF)
- White X symbol
- Multiple icon sizes (16x16 to 256x256)

### 4. **Verify File Structure**
Your repository should look like this:
```
InvokeX/
├── app_installer.py          # Main application
├── install.ps1               # PowerShell installer
├── requirements.txt          # Dependencies
├── run_installer.bat        # Batch file
├── README.md                # Documentation
├── create_icon.py           # Icon generator
├── icon.ico                 # Generated icon
├── .github/
│   ├── workflows/
│   │   └── test-installer.yml
│   └── ISSUE_TEMPLATE/
│       └── bug_report.md
└── SETUP_GUIDE.md           # This file
```

## 🎯 **Key Features of Your Setup**

### **Professional PowerShell Installer**
- **One-line installation**: `irm https://raw.githubusercontent.com/GoblinRules/InvokeX/main/install.ps1 | iex`
- **Automatic Python detection** and installation (no manual intervention needed)
- **Custom installation path**: `C:\Tools\InvokeX`
- **Desktop and Start Menu shortcuts** with custom icon
- **Built-in uninstaller**

### **Enhanced GUI Application**
- **InvokeX branding** throughout the interface
- **Custom window icon** support
- **Comprehensive logging** system
- **Admin privilege management**
- **Auto-scaling and scrollable** interface
- **Installation status indicators**

### **GitHub Integration**
- **Automated testing** with GitHub Actions
- **Professional issue templates**
- **Comprehensive documentation**
- **MIT license** ready

## 🔧 **Testing Your Setup**

### **Local Testing**
```bash
# Test the Python application
python app_installer.py

# Test the PowerShell installer
powershell -ExecutionPolicy Bypass -File install.ps1 -Help

# Generate the icon
python create_icon.py
```

### **GitHub Actions Testing**
- Push your code to trigger automatic testing
- Check the Actions tab for test results
- Verify all files are properly detected

## 📝 **Repository Description**

Use this description for your GitHub repository:

```
Modern GUI installer for Windows applications and system tweaks

InvokeX provides a beautiful, user-friendly interface for installing popular Windows applications and applying system tweaks. Features include real-time logging, auto-scaling, comprehensive error handling, and automatic Python detection and installation.

🚀 One-line installation: irm https://raw.githubusercontent.com/GoblinRules/InvokeX/main/install.ps1 | iex
```

## 🏷️ **Repository Topics**

Add these topics to your repository:
- `windows`
- `gui`
- `installer`
- `python`
- `powershell`
- `system-tweaks`
- `windows-utilities`
- `automation`

## 📄 **License**

Your repository is set up with MIT license. The `app_installer.py` file includes the license header.

## 🌟 **What Users Will Experience**

### **Installation**
```powershell
irm https://raw.githubusercontent.com/GoblinRules/InvokeX/main/install.ps1 | iex
```

### **What Happens Automatically**
1. ✅ **Python Detection** - Automatically finds existing Python installations
2. ✅ **Python Installation** - Installs Python automatically if not found (no user input needed)
3. ✅ **File Download** - Gets all files from your repository
4. ✅ **Installation** - Installs to `C:\Tools\InvokeX`
5. ✅ **Shortcuts** - Creates desktop and start menu shortcuts with custom icon
6. ✅ **Ready to Use** - Professional application ready

### **User Benefits**
- **Zero Python knowledge required** - Everything is automatic
- **Professional appearance** - Custom icon and branding throughout
- **Easy access** - Desktop and start menu shortcuts
- **Clean uninstallation** - Built-in uninstaller
- **Comprehensive logging** - All operations tracked
- **No manual intervention** - Fully automated setup

## 🚀 **Next Steps**

1. **Push all files** to your repository
2. **Test the installer** locally
3. **Create a release** (v1.0.0)
4. **Share the installation command**:
   ```powershell
   irm https://raw.githubusercontent.com/GoblinRules/InvokeX/main/install.ps1 | iex
   ```

## 🎉 **You're Ready!**

Your InvokeX repository is now set up with:
- ✅ **Fully automatic PowerShell installer** (no manual Python setup needed)
- ✅ **Beautiful GUI application** with custom branding
- ✅ **Custom icon system** for professional appearance
- ✅ **Comprehensive documentation** and setup guides
- ✅ **GitHub Actions testing** for quality assurance
- ✅ **Professional issue templates** for user support
- ✅ **MIT license** ready for open source

Users can now install your application with a **single PowerShell command** and get a **completely automated, professional experience** that rivals commercial software!

---

**Need help?** Check the [Issues](https://github.com/GoblinRules/InvokeX/issues) section or create a new issue for support.
