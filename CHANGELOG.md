# Changelog

All notable changes to InvokeX will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-08-20

### ✨ Major Features
- **Complete UI Overhaul**: Migrated from tkinter to CustomTkinter for modern, professional interface
- **Dark/Light Mode**: Automatic theme switching based on system preferences
- **Async Operations**: Non-blocking startup and status checks for improved responsiveness
- **Enhanced Terminal**: Visual feedback with emoji symbols (✅ ❌ ⚠️ ℹ️) and improved formatting
- **Condensed Layout**: More space-efficient card design with reduced padding and better proportions

### 🔧 Improvements
- **Performance**: Async Python detection prevents UI blocking during startup
- **Reliability**: Better error handling for admin privilege operations
- **Visual Feedback**: Real-time status indicators for all applications and tweaks
- **User Experience**: Improved button positioning, colors, and responsive design
- **Terminal Output**: Smaller, scrollable terminal area with properly positioned red clear button

### 🐛 Bug Fixes
- **Admin Crashes**: Fixed application crashes when relaunching as administrator
- **Text Wrapping**: Fixed description text being cut off in headers
- **Color Consistency**: Resolved inconsistent colors between Applications and System Tweaks tabs
- **Legacy Widgets**: Converted remaining tkinter widgets to CustomTkinter for compatibility
- **Startup Issues**: Fixed slow startup and blocking operations

### 🛡️ Security & Stability
- **Safe Widget Operations**: Added error handling to prevent cascading UI failures
- **Admin Detection**: Improved administrator privilege checking and UAC handling
- **Process Management**: Better PowerShell execution with proper window sizing
- **Memory Management**: Optimized widget creation and destruction

### 📖 Documentation
- **Comprehensive README**: Complete rewrite with detailed features, installation, and usage
- **Contributing Guide**: Guidelines for developers and contributors
- **License**: MIT License added for open source compliance
- **Screenshots**: Placeholder structure for visual documentation

### 🔄 Technical Changes
- **Dependencies**: Updated to CustomTkinter 5.2.0+
- **Code Structure**: Improved organization and error handling
- **Logging System**: Enhanced with visual symbols and better formatting
- **UI Components**: All dialogs and popups converted to CustomTkinter

## [1.0.0] - 2024-08-19

### ✨ Initial Release
- **Application Installers**: PyAutoClicker, IP Python Tray App, PowerEventProvider, CTT WinUtil, MASS, Tailscale, MuMu, Ninite
- **System Tweaks**: Hide Shutdown Options, Chrome Default Browser, Power Management, User Account Control, Remote Desktop
- **Basic GUI**: Traditional tkinter interface with functional layout
- **Terminal Output**: Basic logging with timestamps and color coding
- **Admin Support**: Administrator privilege detection and UAC prompts
- **PowerShell Integration**: Execute PowerShell scripts and commands safely

### 🔧 Core Features
- **Status Checking**: Real-time installation and configuration status
- **Download Management**: Automatic file downloads with progress tracking
- **Registry Operations**: Safe registry modifications with error handling
- **Service Management**: Windows service control and monitoring
- **GPO Integration**: Group Policy Object modifications for system tweaks

### 📁 File Structure
- **Main Application**: `app_installer.py` with modular function organization
- **Installation**: PowerShell and batch installers for easy deployment
- **Icon Support**: Custom application icon for branding
- **Logging**: File-based logging system with rotation
- **Backup System**: Registry and configuration backup capabilities

---

## Upcoming Features (Roadmap)

### v2.1.0 (Planned)
- **Plugin System**: Modular architecture for custom installers
- **Configuration Files**: Save/load application preferences
- **Backup/Restore**: Complete system state backup and restore
- **Multi-language**: Support for additional languages
- **Accessibility**: Improved screen reader and keyboard navigation support

### v2.2.0 (Planned)
- **Network Support**: Proxy configuration and offline mode
- **Scheduler**: Automated installation and maintenance tasks
- **Remote Management**: Control multiple systems from single interface
- **Advanced Tweaks**: Additional system optimizations and configurations
- **Theme Customization**: Custom color schemes and layouts

### Future Considerations
- **Package Manager**: Integration with chocolatey, winget, and other package managers
- **Cloud Sync**: Synchronize configurations across devices
- **Enterprise Features**: Group deployment and management tools
- **Mobile Companion**: Android/iOS apps for remote control
- **Web Interface**: Browser-based management portal

---

## Support

- **Bug Reports**: [GitHub Issues](https://github.com/GoblinRules/InvokeX/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/GoblinRules/InvokeX/discussions)
- **Documentation**: [Wiki](https://github.com/GoblinRules/InvokeX/wiki)
- **Community**: [Discussions](https://github.com/GoblinRules/InvokeX/discussions)
