# Contributing to InvokeX

Thank you for your interest in contributing to InvokeX! This document provides guidelines and information for contributors.

## 🤝 Ways to Contribute

### Bug Reports
- Use the [Issues](https://github.com/GoblinRules/InvokeX/issues) page to report bugs
- Include detailed steps to reproduce the issue
- Provide your Windows version and Python version
- Include relevant log files from the `logs/` directory

### Feature Requests
- Submit feature requests via [Issues](https://github.com/GoblinRules/InvokeX/issues)
- Clearly describe the proposed functionality
- Explain the use case and benefits
- Consider backward compatibility

### Code Contributions
- Fork the repository
- Create a feature branch from `main`
- Make your changes following the coding standards below
- Test your changes thoroughly
- Submit a Pull Request with a clear description

## 🛠️ Development Setup

### Prerequisites
- Windows 10/11
- Python 3.7+
- Git
- Text editor or IDE (VS Code recommended)

### Local Development
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/InvokeX.git
cd InvokeX

# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app_installer.py
```

## 📝 Coding Standards

### Python Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and concise
- Use type hints where appropriate

### GUI Development
- Use CustomTkinter for all new GUI components
- Maintain consistent styling with existing interface
- Ensure responsive design for different screen sizes
- Test both light and dark mode themes
- Add proper error handling for UI operations

### Code Structure
```python
def function_name(self, parameter):
    """
    Brief description of what the function does.
    
    Args:
        parameter (type): Description of the parameter
        
    Returns:
        type: Description of return value
    """
    # Implementation
    pass
```

### Logging
- Use the existing logging system
- Add appropriate log levels (INFO, WARNING, ERROR, SUCCESS)
- Log all significant operations
- Include helpful context in log messages

## 🧪 Testing

### Before Submitting
- [ ] Test on Windows 10 and 11 (if possible)
- [ ] Test both standard user and administrator modes
- [ ] Verify all new features work as expected
- [ ] Check that existing functionality isn't broken
- [ ] Test UI responsiveness and theme switching
- [ ] Verify log output is appropriate

### Manual Testing Checklist
- [ ] Application starts without errors
- [ ] All tabs load properly
- [ ] Installation functions work correctly
- [ ] System tweaks apply and restore properly
- [ ] Terminal output is clear and informative
- [ ] Admin privilege handling works correctly

## 📋 Pull Request Process

### Before Creating PR
1. Update documentation if needed
2. Add your changes to the changelog (see format below)
3. Test thoroughly on your local system
4. Ensure code follows the established patterns

### PR Description Should Include
- **Summary**: Brief description of changes
- **Type**: Bug fix, feature, enhancement, etc.
- **Testing**: How you tested the changes
- **Screenshots**: If UI changes are involved
- **Breaking Changes**: Any compatibility issues

### Review Process
- Maintainers will review your PR
- Address any requested changes
- Once approved, your PR will be merged
- Thank you for contributing! 🎉

## 🔄 Changelog Format

Add entries to `CHANGELOG.md` in this format:

```markdown
### Version X.X.X (Date)
- ✨ **New Feature**: Description of feature
- 🐛 **Bug Fix**: Description of fix
- 🔧 **Enhancement**: Description of enhancement
- 📖 **Documentation**: Documentation updates
- ⚡ **Performance**: Performance improvements
```

## 🏷️ Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Documentation improvements
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention is needed
- `question` - Further information is requested
- `wontfix` - This will not be worked on

## 💬 Communication

- Use [Discussions](https://github.com/GoblinRules/InvokeX/discussions) for general questions
- Use [Issues](https://github.com/GoblinRules/InvokeX/issues) for bugs and feature requests
- Keep discussions respectful and constructive
- Be patient with response times

## 📚 Resources

- [CustomTkinter Documentation](https://customtkinter.tomschimansky.com/)
- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Windows API Documentation](https://docs.microsoft.com/en-us/windows/win32/)
- [PowerShell Documentation](https://docs.microsoft.com/en-us/powershell/)

## 🎯 Areas for Contribution

### High Priority
- Application installer improvements
- System tweak safety enhancements  
- Cross-Windows version compatibility
- Performance optimizations
- Accessibility improvements

### Medium Priority
- Additional application installers
- New system tweaks
- UI/UX enhancements
- Documentation improvements
- Test coverage

### Ideas Welcome
- Plugin system architecture
- Configuration file support
- Backup/restore functionality
- Network/proxy support
- Multi-language support

Thank you for helping make InvokeX better! 🚀
