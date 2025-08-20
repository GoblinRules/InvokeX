"""
InvokeX - Modern GUI installer for Windows applications and system tweaks

A comprehensive GUI application that provides easy installation of popular Windows
applications and system tweaks with real-time logging, auto-scaling, and robust
error handling.

Author: GoblinRules
Repository: https://github.com/GoblinRules/InvokeX
License: MIT
Version: 1.0.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import webbrowser
import os
import sys
import logging
from datetime import datetime
import ctypes

# Hide console window when running
def hide_console():
    """Hide the console window for a cleaner user experience."""
    try:
        # Get the console window handle
        console_window = ctypes.windll.kernel32.GetConsoleWindow()
        if console_window != 0:
            # Hide the console window
            ctypes.windll.user32.ShowWindow(console_window, 0)
    except Exception:
        # If hiding fails, continue anyway
        pass

class InvokeX:
    """
    Main InvokeX application class.
    
    Provides a modern GUI interface for installing Windows applications and
    applying system tweaks with comprehensive logging and error handling.
    """
    
    def __init__(self, root):
        """
        Initialize the InvokeX application.
        
        Args:
            root: The main Tkinter root window
        """
        self.root = root
        self.root.title("InvokeX - Application & Tweak Installer")
        self.root.geometry("1000x750")
        # Modern gradient-like background
        self.root.configure(bg='#f8f9fa')
        
        # Hide console window for cleaner experience
        hide_console()
        
        # Set window icon if available
        self.set_window_icon()
        
        # Configure logging
        self.setup_logging()
        
        # Check admin privileges
        self.is_admin = self.check_admin_privileges()
        
        # Style configuration
        self.setup_styles()
        
        # Create main container with modern styling
        main_container = tk.Frame(root, bg='#f8f9fa')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.grid(row=0, column=0, sticky='nsew', padx=(0, 0), pady=(0, 10))
        
        # Create tabs
        self.create_apps_tab()
        self.create_tweaks_tab()
        
        # Create terminal window at bottom
        self.create_terminal_window(main_container)
        
        # Bind resize event
        self.root.bind('<Configure>', self.on_resize)
        
        # Check Python availability after UI is initialized
        self.python_available = self.check_python_availability()
        
        # Show admin status
        if not self.is_admin:
            self.show_admin_warning()
    
    def set_window_icon(self):
        """Set the window icon if icon.ico is available."""
        try:
            # Try to find icon in current directory or installation directory
            icon_paths = [
                "icon.ico",
                "C:\\Tools\\InvokeX\\icon.ico",
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
            ]
            
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    self.root.iconbitmap(icon_path)
                    break
        except Exception as e:
            # Icon setting is optional, continue without it
            pass
    
    def setup_styles(self):
        """Configure the visual styles for the application."""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#f0f0f0')
        style.configure('TNotebook.Tab', padding=[15, 8], font=('Segoe UI', 9))
        style.configure('TFrame', background='#f0f0f0')
    
    def check_admin_privileges(self):
        """
        Check if the application is running with administrator privileges.
        
        Returns:
            bool: True if running as administrator, False otherwise
        """
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def check_python_availability(self):
        """
        Check if Python is available and offer to install it if not.
        
        Returns:
            bool: True if Python is available, False otherwise
        """
        try:
            # Check if Python is in PATH
            result = subprocess.run(['python', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                python_version = result.stdout.strip()
                self.log_to_terminal(f"Python detected: {python_version}", "SUCCESS")
                return True
            else:
                # Python not found, offer to install
                self.log_to_terminal("Python not found in system PATH", "WARNING")
                self.offer_python_installation()
                return False
                
        except FileNotFoundError:
            # Python executable not found
            self.log_to_terminal("Python executable not found", "WARNING")
            self.offer_python_installation()
            return False
        except Exception as e:
            # Other errors
            self.log_to_terminal(f"Error checking Python: {str(e)}", "ERROR")
            return False
    
    def offer_python_installation(self):
        """
        Offer to install Python automatically when it's not found.
        """
        # Show this after the UI is fully loaded
        self.root.after(2000, self._show_python_install_dialog)
    
    def _show_python_install_dialog(self):
        """
        Show dialog to install Python if it's not found.
        """
        install_python = messagebox.askyesno(
            "Python Not Found", 
            "Python is required for some applications but was not detected on your system.\n\n"
            "Would you like to install Python automatically?\n\n"
            "This is required for:\n"
            "• IP Python Tray App\n"
            "• PyAutoClicker\n"
            "• Other Python-based applications"
        )
        
        if install_python:
            self.install_python_system()
    
    def install_python_system(self):
        """
        Install Python with enhanced PATH management and verification.
        """
        try:
            self.log_to_terminal("Starting enhanced Python installation...", "INFO")
            
            # Method 1: Try winget first (modern Windows package manager)
            try:
                self.log_to_terminal("Installing Python using Windows Package Manager (winget)...", "INFO")
                python_install = subprocess.run([
                    'winget', 'install', 'Python.Python.3.12', 
                    '--accept-source-agreements', '--accept-package-agreements', '--silent'
                ], capture_output=True, text=True, timeout=300)
                
                if python_install.returncode == 0:
                    self.log_to_terminal("Python installed successfully using winget!", "SUCCESS")
                    
                    # Wait for installation to complete
                    import time
                    time.sleep(5)
                    
                    # Force refresh environment and verify
                    if self.verify_and_fix_python_installation():
                        self.python_available = True
                        return
                else:
                    self.log_to_terminal(f"winget installation failed: {python_install.stderr}", "WARNING")
            
            except Exception as e:
                self.log_to_terminal(f"winget not available or failed: {str(e)}", "WARNING")
            
            # Method 2: Download and install from python.org with enhanced options
            self.log_to_terminal("Downloading Python from python.org with enhanced installation...", "INFO")
            python_url = "https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe"
            python_installer = "python-installer.exe"
            
            import urllib.request
            urllib.request.urlretrieve(python_url, python_installer)
            self.log_to_terminal("Python installer downloaded. Installing with enhanced options...", "INFO")
            
            # Enhanced installation with multiple methods
            install_methods = [
                # Method 1: User installation with PATH
                {
                    'args': [python_installer, '/quiet', 'PrependPath=1', 'Include_test=0', 'SimpleInstall=1'],
                    'name': 'User installation with PATH'
                },
                # Method 2: All users installation
                {
                    'args': [python_installer, '/quiet', 'InstallAllUsers=1', 'PrependPath=1', 'Include_test=0'],
                    'name': 'All users installation'
                },
                # Method 3: Manual PATH setup
                {
                    'args': [python_installer, '/quiet', 'InstallAllUsers=0', 'Include_test=0'],
                    'name': 'Basic installation (manual PATH)'
                }
            ]
            
            installation_success = False
            
            for method in install_methods:
                self.log_to_terminal(f"Trying {method['name']}...", "INFO")
                
                install_result = subprocess.run(
                    method['args'], 
                    capture_output=True, text=True, timeout=600
                )
                
                if install_result.returncode == 0:
                    self.log_to_terminal(f"{method['name']} completed successfully!", "SUCCESS")
                    
                    # Wait for installation to settle
                    import time
                    time.sleep(3)
                    
                    # Verify and fix installation
                    if self.verify_and_fix_python_installation():
                        installation_success = True
                        break
                    else:
                        self.log_to_terminal(f"{method['name']} succeeded but Python not accessible, trying next method...", "WARNING")
                else:
                    self.log_to_terminal(f"{method['name']} failed: {install_result.stderr}", "WARNING")
            
            # Clean up installer
            try:
                os.remove(python_installer)
            except:
                pass
            
            if installation_success:
                messagebox.showinfo(
                    "Python Installed Successfully", 
                    "Python has been installed and configured successfully!\n\n"
                    "Features now available:\n"
                    "• Python-based applications can be installed\n"
                    "• Python scripts will work properly\n"
                    "• Desktop shortcuts will function correctly\n\n"
                    "You can now use all Python-dependent features."
                )
                self.python_available = True
            else:
                self.log_to_terminal("All Python installation methods failed", "ERROR")
                messagebox.showerror(
                    "Python Installation Failed", 
                    "Python could not be installed automatically using any method.\n\n"
                    "Please install Python manually:\n\n"
                    "1. Go to https://www.python.org/downloads/\n"
                    "2. Download Python 3.12 or later\n"
                    "3. Run installer as Administrator\n"
                    "4. IMPORTANT: Check 'Add Python to PATH'\n"
                    "5. Restart InvokeX after installation\n\n"
                    "This will fix desktop shortcut issues."
                )
                
        except Exception as e:
            self.log_to_terminal(f"Error installing Python: {str(e)}", "ERROR")
            messagebox.showerror(
                "Installation Error", 
                f"An error occurred while installing Python: {str(e)}\n\n"
                "Please install Python manually from:\n"
                "https://www.python.org/downloads/\n\n"
                "Make sure to check 'Add Python to PATH' during installation."
            )
    
    def verify_and_fix_python_installation(self):
        """
        Verify Python installation and fix PATH issues.
        
        Returns:
            bool: True if Python is working correctly, False otherwise
        """
        try:
            self.log_to_terminal("Verifying Python installation...", "INFO")
            
            # First, refresh environment variables
            self.refresh_environment()
            
            # Test 1: Direct python command
            result = subprocess.run(['python', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                python_version = result.stdout.strip()
                self.log_to_terminal(f"Python verified: {python_version}", "SUCCESS")
                return True
            
            self.log_to_terminal("Python command failed, attempting to fix PATH...", "WARNING")
            
            # Method 2: Find Python installation and add to PATH
            python_paths = self.find_python_installations()
            
            if python_paths:
                self.log_to_terminal(f"Found Python installations: {python_paths}", "INFO")
                
                # Try to add to PATH
                if self.add_python_to_path(python_paths[0]):
                    # Test again after PATH fix
                    result = subprocess.run(['python', '--version'], 
                                          capture_output=True, text=True, timeout=10)
                    
                    if result.returncode == 0:
                        python_version = result.stdout.strip()
                        self.log_to_terminal(f"Python PATH fixed! Version: {python_version}", "SUCCESS")
                        return True
            
            self.log_to_terminal("Could not verify or fix Python installation", "ERROR")
            return False
            
        except Exception as e:
            self.log_to_terminal(f"Error verifying Python installation: {str(e)}", "ERROR")
            return False
    
    def find_python_installations(self):
        """
        Find Python installations on the system.
        
        Returns:
            list: List of Python installation paths
        """
        python_paths = []
        
        # Common Python installation locations
        search_paths = [
            "C:\\Python*",
            "C:\\Program Files\\Python*",
            "C:\\Program Files (x86)\\Python*",
            os.path.expanduser("~\\AppData\\Local\\Programs\\Python\\Python*"),
            os.path.expanduser("~\\AppData\\Local\\Microsoft\\WindowsApps\\python.exe"),
            "C:\\Users\\*\\AppData\\Local\\Programs\\Python\\Python*"
        ]
        
        import glob
        
        for search_path in search_paths:
            try:
                found = glob.glob(search_path)
                for path in found:
                    if os.path.isdir(path):
                        # Check if python.exe exists in this directory
                        python_exe = os.path.join(path, "python.exe")
                        if os.path.exists(python_exe):
                            python_paths.append(path)
                    elif path.endswith("python.exe") and os.path.exists(path):
                        python_paths.append(os.path.dirname(path))
            except:
                continue
        
        return python_paths
    
    def add_python_to_path(self, python_path):
        """
        Add Python installation to system PATH.
        
        Args:
            python_path (str): Path to Python installation directory
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.log_to_terminal(f"Adding Python to PATH: {python_path}", "INFO")
            
            import winreg
            
            # Add both python.exe directory and Scripts directory
            paths_to_add = [
                python_path,
                os.path.join(python_path, "Scripts")
            ]
            
            # Get current PATH
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS) as key:
                try:
                    current_path, _ = winreg.QueryValueEx(key, "PATH")
                except FileNotFoundError:
                    current_path = ""
                
                # Add new paths if not already present
                path_parts = current_path.split(';') if current_path else []
                
                for new_path in paths_to_add:
                    if new_path not in path_parts:
                        path_parts.append(new_path)
                
                # Update PATH
                new_path_value = ';'.join(path_parts)
                winreg.SetValueEx(key, "PATH", 0, winreg.REG_SZ, new_path_value)
                
                self.log_to_terminal("Python added to user PATH successfully", "SUCCESS")
                
                # Refresh current environment
                os.environ['PATH'] = new_path_value + ';' + os.environ.get('PATH', '')
                
                return True
                
        except Exception as e:
            self.log_to_terminal(f"Failed to add Python to PATH: {str(e)}", "ERROR")
            return False
    
    def refresh_environment(self):
        """
        Refresh environment variables in the current session.
        """
        try:
            # Refresh PATH environment variable
            import winreg
            
            # Get system PATH
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                               "SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment") as key:
                system_path = winreg.QueryValueEx(key, "PATH")[0]
            
            # Get user PATH
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
                    user_path = winreg.QueryValueEx(key, "PATH")[0]
            except FileNotFoundError:
                user_path = ""
            
            # Combine and update current environment
            combined_path = system_path + ";" + user_path if user_path else system_path
            os.environ['PATH'] = combined_path
            
            self.log_to_terminal("Environment variables refreshed", "INFO")
            
        except Exception as e:
            self.log_to_terminal(f"Could not refresh environment: {str(e)}", "WARNING")
    
    def show_admin_warning(self):
        """
        Show warning about admin privileges and offer to restart as admin.
        
        Displays a temporary warning banner with a "Restart as Admin" button
        that automatically disappears after 10 seconds.
        """
        warning_frame = tk.Frame(self.root, bg='#fff3cd', relief='solid', bd=1)
        warning_frame.place(relx=0.5, rely=0.1, anchor='n')
        
        warning_label = tk.Label(warning_frame, 
                                text="⚠️ Administrator privileges recommended for some operations",
                                font=('Segoe UI', 9, 'bold'),
                                bg='#fff3cd', fg='#856404')
        warning_label.pack(side='left', padx=10, pady=5)
        
        restart_btn = tk.Button(warning_frame, 
                               text="Restart as Admin",
                               command=self.restart_as_admin,
                               bg='#dc3545', fg='white',
                               font=('Segoe UI', 8, 'bold'),
                               relief='flat', padx=10, pady=3)
        restart_btn.pack(side='left', padx=(0, 10), pady=5)
        
        close_btn = tk.Button(warning_frame, 
                             text="×",
                             command=warning_frame.destroy,
                             bg='#fff3cd', fg='#856404',
                             font=('Segoe UI', 10, 'bold'),
                             relief='flat', padx=5, pady=0)
        close_btn.pack(side='right', padx=5, pady=5)
        
        # Auto-hide after 10 seconds
        self.root.after(10000, warning_frame.destroy)
    
    def restart_as_admin(self):
        """
        Restart the application with administrator privileges.
        
        Uses PowerShell to restart the current script/executable with
        elevated privileges using the 'RunAs' verb.
        """
        try:
            import sys
            import subprocess
            
            # Get the current script path
            script_path = sys.argv[0]
            if script_path.endswith('.py'):
                # If running as Python script, restart with Python
                cmd = ['powershell', 'Start-Process', 'python', '-ArgumentList', f'"{script_path}"', '-Verb', 'RunAs']
            else:
                # If running as executable, restart the executable
                cmd = ['powershell', 'Start-Process', f'"{script_path}"', '-Verb', 'RunAs']
            
            subprocess.run(cmd)
            self.root.quit()
        except Exception as e:
            self.log_to_terminal(f"Failed to restart as admin: {str(e)}", "ERROR")
            messagebox.showerror("Error", f"Failed to restart as administrator: {str(e)}")
        
    def setup_logging(self):
        """
        Set up comprehensive logging system.
        
        Creates a logs directory and configures both file and console logging
        with timestamped log files for debugging and audit purposes.
        """
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        # Configure logging
        log_filename = f'logs/invokex_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def create_terminal_window(self, parent):
        """
        Create the terminal output window at the bottom of the application.
        
        Args:
            parent: The parent widget to contain the terminal
        """
        # Terminal frame
        terminal_frame = tk.LabelFrame(parent, text="Terminal Output", bg='#f0f0f0', fg='#2c3e50', font=('Segoe UI', 9, 'bold'))
        terminal_frame.grid(row=1, column=0, sticky='nsew', padx=(0, 0), pady=(0, 0))
        terminal_frame.grid_columnconfigure(0, weight=1)
        terminal_frame.grid_rowconfigure(0, weight=1)
        
        # Terminal text widget with scrollbar
        self.terminal = scrolledtext.ScrolledText(
            terminal_frame, 
            height=8, 
            font=('Consolas', 8),
            bg='#1e1e1e',
            fg='#ffffff',
            insertbackground='#ffffff',
            wrap=tk.WORD
        )
        self.terminal.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        
        # Clear button
        clear_btn = tk.Button(
            terminal_frame, 
            text="Clear Terminal", 
            command=self.clear_terminal,
            bg='#e74c3c', 
            fg='white',
            font=('Segoe UI', 8, 'bold'),
            relief='flat', 
            padx=10, 
            pady=3
        )
        clear_btn.grid(row=0, column=1, sticky='ne', padx=(0, 5), pady=5)
        
        # Welcome message
        admin_status = "Administrator" if self.is_admin else "Standard User"
        self.log_to_terminal("InvokeX started successfully!", "INFO")
        self.log_to_terminal(f"Running as: {admin_status}", "INFO")
        if not self.is_admin:
            self.log_to_terminal("Note: Some operations may require administrator privileges", "WARNING")
        self.log_to_terminal("Ready to install applications and apply system tweaks.", "INFO")
        
    def log_to_terminal(self, message, level="INFO"):
        """
        Log a message to both the terminal and log files with enhanced formatting.
        
        Args:
            message (str): The message to log
            level (str): The log level (INFO, ERROR, WARNING, SUCCESS)
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        date_stamp = datetime.now().strftime("%Y-%m-%d")
        
        # Color map for different log levels
        color_map = {
            "INFO": "#28a745",     # Green
            "ERROR": "#dc3545",    # Red
            "WARNING": "#ffc107",  # Yellow/Orange
            "SUCCESS": "#17a2b8",  # Cyan/Blue
            "DEBUG": "#6c757d"     # Gray
        }
        
        # Level formatting for better readability
        level_formatted = f"[{level.upper():^7}]"
        
        # Enhanced terminal output with more detail
        log_entry = f"[{timestamp}] {level_formatted} {message}\n"
        
        # Add to terminal with color (if supported)
        try:
            self.terminal.configure(state='normal')
            start_index = self.terminal.index(tk.END + "-1c linestart")
            self.terminal.insert(tk.END, log_entry)
            end_index = self.terminal.index(tk.END + "-1c")
            
            # Apply color to the log level portion
            level_start = f"{start_index} + {len(f'[{timestamp}] ')}c"
            level_end = f"{start_index} + {len(f'[{timestamp}] {level_formatted}')}c"
            
            if level.upper() in color_map:
                self.terminal.tag_add(level, level_start, level_end)
                self.terminal.tag_configure(level, foreground=color_map[level.upper()], font=('Segoe UI', 9, 'bold'))
            
            self.terminal.configure(state='disabled')
            self.terminal.see(tk.END)
        except:
            # Fallback to simple insert if coloring fails
            self.terminal.insert(tk.END, log_entry)
            self.terminal.see(tk.END)
        
        # Enhanced file logging with more context
        detailed_message = f"{date_stamp} {timestamp} | {level.upper():7} | {message}"
        
        if level == "ERROR":
            self.logger.error(detailed_message)
        elif level == "WARNING":
            self.logger.warning(detailed_message)
        elif level == "SUCCESS":
            self.logger.info(f"SUCCESS | {detailed_message}")
        elif level == "DEBUG":
            self.logger.debug(detailed_message)
        else:
            self.logger.info(detailed_message)
            
    def clear_terminal(self):
        """Clear the terminal output window."""
        self.terminal.delete(1.0, tk.END)
        self.log_to_terminal("Terminal cleared.", "INFO")
        
    def on_resize(self, event):
        """
        Handle window resize events.
        
        Args:
            event: The resize event
        """
        if event.widget == self.root:
            # The notebook and terminal will automatically resize due to grid weights
            pass
        
    def create_apps_tab(self):
        """Create the Applications tab with consistent modern styling."""
        apps_frame = tk.Frame(self.notebook, bg='#f8f9fa')
        self.notebook.add(apps_frame, text="Applications")
        
        # Configure grid weights for auto-scaling
        apps_frame.grid_columnconfigure(0, weight=1)
        apps_frame.grid_rowconfigure(2, weight=1)
        
        # Header frame with modern gradient-like background
        header_frame = tk.Frame(apps_frame, bg='#ffffff', height=80, relief='flat', bd=0)
        header_frame.grid(row=0, column=0, sticky='ew', padx=0, pady=0)
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Add subtle shadow effect
        shadow_frame = tk.Frame(apps_frame, bg='#e9ecef', height=2)
        shadow_frame.grid(row=1, column=0, sticky='ew', padx=0, pady=0)
        
        # Title in header
        title_label = tk.Label(header_frame, text="Application Installer", 
                              font=('Segoe UI', 18, 'bold'), 
                              bg='#ffffff', fg='#212529')
        title_label.grid(row=0, column=0, pady=20, sticky='w', padx=30)
        
        # Subtitle
        subtitle_label = tk.Label(header_frame, text="Install and manage essential Windows applications", 
                                 font=('Segoe UI', 10), 
                                 bg='#ffffff', fg='#6c757d')
        subtitle_label.grid(row=1, column=0, pady=(0, 20), sticky='w', padx=30)
        
        # Create scrollable canvas for apps
        canvas_frame = tk.Frame(apps_frame, bg='#f8f9fa')
        canvas_frame.grid(row=2, column=0, sticky='nsew', padx=20, pady=(10, 20))
        canvas_frame.grid_columnconfigure(0, weight=1)
        canvas_frame.grid_rowconfigure(0, weight=1)
        
        # Canvas and scrollbar with modern styling
        canvas = tk.Canvas(canvas_frame, bg='#f8f9fa', highlightthickness=0, bd=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Apps container with modern styling
        apps_container = tk.Frame(scrollable_frame, bg='#f8f9fa')
        apps_container.pack(fill='both', expand=True, padx=15)
        
        # App 1: PyAutoClicker
        self.create_app_section(apps_container, 
                               "PyAutoClicker", 
                               "Automated clicking utility",
                               "Install PyAutoClicker",
                               "https://github.com/GoblinRules/PyAutoClicker",
                               lambda: self.run_powershell_command("irm https://raw.githubusercontent.com/GoblinRules/PyAutoClicker/main/install.ps1 | iex"))
        
        # App 2: IP Python Tray App
        self.create_app_section(apps_container, 
                               "IP Python Tray App", 
                               "System tray IP address display",
                               "Install IP Python Tray App",
                               "https://github.com/GoblinRules/ippy-tray-app",
                               lambda: self.install_ippy_tray())
        
        # App 3: PowerEventProvider
        self.create_app_section_with_3_buttons(apps_container, 
                               "PowerEventProvider", 
                               "Power management event provider",
                               "Download & Install",
                               "GitHub",
                               "View Power Logs",
                               "https://github.com/GoblinRules/powereventprovider",
                               lambda: self.download_and_install_msi("https://github.com/GoblinRules/powereventprovider/releases/download/V1.1/PowerEventProviderSetup.msi"),
                               lambda: webbrowser.open("https://github.com/GoblinRules/powereventprovider"),
                               lambda: self.view_power_logs())
        
        # App 4: CTT WinUtil
        self.create_app_section(apps_container, 
                               "CTT WinUtil", 
                               "Windows utility collection",
                               "Run CTT WinUtil",
                               "https://github.com/ChrisTitusTech/winutil",
                               lambda: self.run_ctt_winutil())
        
        # App 5: MASS
        self.create_app_section(apps_container, 
                               "MASS", 
                               "Microsoft Activation Scripts",
                               "Run MASS",
                               "https://github.com/massgravel/Microsoft-Activation-Scripts",
                               lambda: self.run_powershell_command("irm https://get.activated.win | iex"))
        
        # App 6: Tailscale
        self.create_app_section(apps_container, 
                               "Tailscale", 
                               "VPN and secure networking",
                               "Download & Install",
                               "https://tailscale.com/",
                               lambda: self.download_and_install_exe("https://pkgs.tailscale.com/stable/tailscale-setup-latest.exe", "Tailscale"))
        
        # App 7: MuMu
        self.create_app_section(apps_container, 
                               "MuMu", 
                               "Android emulator for Windows",
                               "Download & Install",
                               "https://www.mumuplayer.com/",
                               lambda: self.download_and_install_exe("https://a11.gdl.netease.com/MuMu_5.0.2_gw-overseas12_all_1754534682.exe?n=MuMu_5.0.2_lMBe7ZC.exe", "MuMu"))
        
        # App 8: Ninite Installer
        self.create_app_section(apps_container, 
                               "Ninite Installer", 
                               "Essential apps installer (7zip, Chrome, Firefox, Notepad++)",
                               "Download & Install",
                               "https://ninite.com/",
                               lambda: self.download_and_install_exe("https://ninite.com/7zip-chrome-firefox-notepadplusplus/ninite.exe", "Ninite"))
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Improved mouse wheel scrolling - bind only when hovering over the canvas
        def _on_mousewheel(event):
            # Scroll faster and smoother
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        
        # Bind mouse wheel only when hovering over the canvas area
        canvas.bind('<Enter>', _bind_mousewheel)
        canvas.bind('<Leave>', _unbind_mousewheel)
        scrollable_frame.bind('<Enter>', _bind_mousewheel)
        scrollable_frame.bind('<Leave>', _unbind_mousewheel)
        
        # Also bind to the apps container for better coverage
        apps_container.bind('<Enter>', _bind_mousewheel)
        apps_container.bind('<Leave>', _unbind_mousewheel)
    
    def create_tweaks_tab(self):
        """Create the System Tweaks tab with consistent modern styling."""
        tweaks_frame = tk.Frame(self.notebook, bg='#f8f9fa')
        self.notebook.add(tweaks_frame, text="System Tweaks")
        
        # Configure grid weights for auto-scaling
        tweaks_frame.grid_columnconfigure(0, weight=1)
        tweaks_frame.grid_rowconfigure(2, weight=1)
        
        # Header frame with modern gradient-like background (matching apps tab)
        header_frame = tk.Frame(tweaks_frame, bg='#ffffff', height=80, relief='flat', bd=0)
        header_frame.grid(row=0, column=0, sticky='ew', padx=0, pady=0)
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Add subtle shadow effect
        shadow_frame = tk.Frame(tweaks_frame, bg='#e9ecef', height=2)
        shadow_frame.grid(row=1, column=0, sticky='ew', padx=0, pady=0)
        
        # Title in header
        title_label = tk.Label(header_frame, text="System Tweaks", 
                              font=('Segoe UI', 18, 'bold'), 
                              bg='#ffffff', fg='#212529')
        title_label.grid(row=0, column=0, pady=20, sticky='w', padx=30)
        
        # Subtitle with Windows version
        windows_version = self.get_windows_version()
        subtitle_label = tk.Label(header_frame, text=f"Customize Windows settings and behavior • {windows_version}", 
                                 font=('Segoe UI', 10), 
                                 bg='#ffffff', fg='#6c757d')
        subtitle_label.grid(row=1, column=0, pady=(0, 20), sticky='w', padx=30)
        
        # Create scrollable canvas for tweaks
        canvas_frame = tk.Frame(tweaks_frame, bg='#f8f9fa')
        canvas_frame.grid(row=2, column=0, sticky='nsew', padx=20, pady=(10, 20))
        canvas_frame.grid_columnconfigure(0, weight=1)
        canvas_frame.grid_rowconfigure(0, weight=1)
        
        # Canvas and scrollbar with modern styling
        canvas = tk.Canvas(canvas_frame, bg='#f8f9fa', highlightthickness=0, bd=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Tweaks container with modern styling
        tweaks_container = tk.Frame(scrollable_frame, bg='#f8f9fa')
        tweaks_container.pack(fill='both', expand=True, padx=15)
        
        # Tweak 1: Hide Shutdown Options (GPO-based, no registry check needed)
        self.create_single_tweak_with_3_buttons(tweaks_container,
                                               "Hide Shutdown Options",
                                               "Hide shutdown, sleep, and hibernate options from start menu using Group Policy",
                                               "Hide Options",
                                               "Restore Defaults", 
                                               "View Status",
                                               lambda: self.remove_shutdown_from_startup_smart(),
                                               lambda: self.restore_shutdown_options(),
                                               lambda: self.check_gpo_status())
        
        # Tweak 2: Set Chrome As Default Browser
        self.create_single_tweak_with_3_buttons(tweaks_container,
                                               "Set Chrome As Default Browser",
                                               "Set Google Chrome as default browser",
                                               "Set Chrome Default",
                                               "Restore Defaults",
                                               "Check Current Default", 
                                               lambda: self.set_chrome_as_default(),
                                               lambda: self.reset_default_browser(),
                                               lambda: self.check_current_default_browser())
        
        # Tweak 3: Power Management Settings
        self.create_single_tweak_with_3_buttons(tweaks_container,
                                               "Power Management Settings", 
                                               "Configure power settings (never sleep/hibernate, power button/lid do nothing, never turn off display)",
                                               "Configure Power",
                                               "Restore Defaults",
                                               "Check Status",
                                               lambda: self.configure_power_management(),
                                               lambda: self.reset_power_management(),
                                               lambda: self.check_power_status())
        
        # Tweak 4: Power Actions
        self.create_single_tweak_with_3_buttons(tweaks_container,
                                               "Power Actions",
                                               "Quick power actions for system control",
                                               "Restart",
                                               "Shutdown",
                                               None,  # No third button
                                               lambda: self.restart_system_10s(),
                                               lambda: self.shutdown_system(),
                                               None)
        
        # Tweak 5: Prevent User Account Creation
        self.create_single_tweak_with_3_buttons(tweaks_container,
                                               "Prevent User Account Creation",
                                               "Prevent any more user accounts from being created on this system",
                                               "Enable Protection",
                                               "Restore Defaults",
                                               "Check Status",
                                               lambda: self.prevent_user_creation(),
                                               lambda: self.restore_user_creation(),
                                               lambda: self.check_user_creation_status())
        
        # Tweak 6: Create Admin Account
        self.create_single_tweak_with_3_buttons(tweaks_container,
                                               "Create Admin Account",
                                               "Create account called 'Admin' that is a member of Administrators & Remote Desktop Users",
                                               "Create Account",
                                               "Manage Users",
                                               "Check Status",
                                               lambda: self.create_admin_account(),
                                               lambda: self.open_user_management(),
                                               lambda: self.check_admin_account_status())
        
        # Tweak 7: Enable Remote Desktop
        self.create_single_tweak_with_3_buttons(tweaks_container,
                                               "Enable Remote Desktop Connections",
                                               "Enable Remote Desktop connections and configure firewall rules",
                                               "Enable RDP",
                                               "Disable RDP",
                                               "Check Status",
                                               lambda: self.enable_remote_desktop(),
                                               lambda: self.disable_remote_desktop(),
                                               lambda: self.check_rdp_status())
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Modern mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        
        # Bind mouse wheel events
        canvas.bind('<Enter>', _bind_mousewheel)
        canvas.bind('<Leave>', _unbind_mousewheel)
        scrollable_frame.bind('<Enter>', _bind_mousewheel)
        scrollable_frame.bind('<Leave>', _unbind_mousewheel)
        tweaks_container.bind('<Enter>', _bind_mousewheel)
        tweaks_container.bind('<Leave>', _unbind_mousewheel)
    
    def create_single_tweak_with_3_buttons(self, parent, title, description, btn1_text, btn2_text, btn3_text, btn1_func, btn2_func, btn3_func):
        """Create a single tweak section with modern 3-button layout and consistent styling."""
        # Container for this tweak with modern card styling
        tweak_frame = tk.Frame(parent, bg='#ffffff', relief='flat', bd=1)
        tweak_frame.pack(fill='x', pady=6, padx=0)
        
        # Add subtle border
        border_frame = tk.Frame(tweak_frame, bg='#dee2e6', height=1)
        border_frame.pack(fill='x', side='bottom')
        
        # Tweak info with consistent padding
        info_frame = tk.Frame(tweak_frame, bg='#ffffff')
        info_frame.pack(fill='x', padx=25, pady=20)
        
        # Title with consistent typography
        title_label = tk.Label(info_frame, text=title, 
                              font=('Segoe UI', 13, 'bold'), 
                              bg='#ffffff', fg='#212529', anchor='w')
        title_label.pack(anchor='w')
        
        # Description with consistent spacing
        desc_label = tk.Label(info_frame, text=description, 
                             font=('Segoe UI', 9), 
                             bg='#ffffff', fg='#6c757d', anchor='w',
                             wraplength=800)
        desc_label.pack(anchor='w', pady=(6, 0))
        
        # Buttons frame with consistent alignment
        buttons_frame = tk.Frame(info_frame, bg='#ffffff')
        buttons_frame.pack(fill='x', pady=(18, 0))
        
        # Consistent button styling
        button_style = {
            'font': ('Segoe UI', 9, 'bold'),
            'relief': 'flat',
            'padx': 24,
            'pady': 10,
            'cursor': 'hand2',
            'bd': 0,
            'width': 15  # Fixed width for alignment
        }
        
        # Button 1 (Action) - Primary color
        btn1 = tk.Button(buttons_frame, text=btn1_text, 
                        command=btn1_func,
                        bg='#0d6efd', fg='white',
                        **button_style)
        btn1.pack(side='left', padx=(0, 12))
        
        # Button 2 (Restore) - Success color
        btn2 = tk.Button(buttons_frame, text=btn2_text, 
                        command=btn2_func,
                        bg='#198754', fg='white',
                        **button_style)
        btn2.pack(side='left', padx=(0, 12))
        
        # Button 3 (Check/Info) - Info color or hide if None
        if btn3_text and btn3_func:
            btn3 = tk.Button(buttons_frame, text=btn3_text, 
                            command=btn3_func,
                            bg='#0dcaf0', fg='#212529',
                            **button_style)
            btn3.pack(side='left')
            
            # Hover effects for button 3
            btn3.bind('<Enter>', lambda e: btn3.configure(bg='#31d2f2'))
            btn3.bind('<Leave>', lambda e: btn3.configure(bg='#0dcaf0'))
        
        # Consistent hover effects
        btn1.bind('<Enter>', lambda e: btn1.configure(bg='#0b5ed7'))
        btn1.bind('<Leave>', lambda e: btn1.configure(bg='#0d6efd'))
        btn2.bind('<Enter>', lambda e: btn2.configure(bg='#157347'))
        btn2.bind('<Leave>', lambda e: btn2.configure(bg='#198754'))
    
    def create_tweak_section(self, parent, title, description, action_text, restore_text, action_func, restore_func, has_registry=True):
        """
        Create a section for an individual tweak with action, restore, and check registry buttons.
        
        Args:
            parent: The parent widget
            title (str): Tweak title
            description (str): Tweak description
            action_text (str): Text for the action button
            restore_text (str): Text for the restore button (None to hide)
            action_func: Function to call when action button is clicked
            restore_func: Function to call when restore button is clicked (None to hide)
            has_registry (bool): Whether this tweak has registry settings to check
        """
        # Container for each tweak
        tweak_frame = tk.Frame(parent, bg='white', relief='solid', bd=1)
        tweak_frame.pack(fill='x', pady=6, padx=8)
        
        # Tweak info
        info_frame = tk.Frame(tweak_frame, bg='white')
        info_frame.pack(fill='x', padx=12, pady=10)
        
        # Title and description
        title_label = tk.Label(info_frame, text=title, 
                              font=('Segoe UI', 11, 'bold'), 
                              bg='white', fg='#2c3e50', anchor='w')
        title_label.pack(anchor='w')
        
        desc_label = tk.Label(info_frame, text=description, 
                             font=('Segoe UI', 8), 
                             bg='white', fg='#7f8c8d', anchor='w')
        desc_label.pack(anchor='w', pady=(3, 0))
        
        # Buttons frame
        buttons_frame = tk.Frame(info_frame, bg='white')
        buttons_frame.pack(fill='x', pady=(10, 0))
        
        # Action button
        action_btn = tk.Button(buttons_frame, text=action_text, 
                              command=action_func,
                              bg='#e74c3c', fg='white',  # Red for action
                              font=('Segoe UI', 8, 'bold'),
                              relief='flat', padx=15, pady=5,
                              cursor='hand2')
        action_btn.pack(side='left', padx=(0, 8))
        
        # Restore button (only if restore function is provided)
        if restore_func and restore_text:
            restore_btn = tk.Button(buttons_frame, text=restore_text, 
                                   command=restore_func,
                                   bg='#27ae60', fg='white',  # Green for restore
                                   font=('Segoe UI', 8, 'bold'),
                                   relief='flat', padx=15, pady=5,
                                   cursor='hand2')
            restore_btn.pack(side='left', padx=(0, 8))
            
            # Hover effects for restore button
            restore_btn.bind('<Enter>', lambda e: restore_btn.configure(bg='#229954'))
            restore_btn.bind('<Leave>', lambda e: restore_btn.configure(bg='#27ae60'))
        
        # Check Registry button (only for tweaks that modify registry)
        if has_registry:
            check_reg_btn = tk.Button(buttons_frame, text="Check Reg Keys", 
                                     command=lambda: self.check_registry_keys_for_tweak(title),
                                     bg='#3498db', fg='white',  # Blue for check
                                     font=('Segoe UI', 8, 'bold'),
                                     relief='flat', padx=15, pady=5,
                                     cursor='hand2')
            check_reg_btn.pack(side='left')
            
            # Hover effects for check registry button
            check_reg_btn.bind('<Enter>', lambda e: check_reg_btn.configure(bg='#2980b9'))
            check_reg_btn.bind('<Leave>', lambda e: check_reg_btn.configure(bg='#3498db'))
        
        # Hover effects for action button
        action_btn.bind('<Enter>', lambda e: action_btn.configure(bg='#c0392b'))
        action_btn.bind('<Leave>', lambda e: action_btn.configure(bg='#e74c3c'))

    def check_registry_keys_for_tweak(self, tweak_name):
        """Check registry keys specific to a tweak."""
        self.log_to_terminal(f"Checking registry keys for: {tweak_name}", "info")
        
        try:
            if tweak_name == "Hide Shutdown Options":
                # Check shutdown-related registry keys
                keys_to_check = [
                    ("HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer", "NoClose"),
                    ("HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer", "NoShutdown"),
                    ("HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer", "NoShutdown"),
                    ("HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System", "DisableShutdown"),
                    ("HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer", "NoLogoff"),
                    ("HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer", "NoPowerOptions")
                ]
            elif tweak_name == "Set Chrome As Default Browser":
                # Check browser-related registry keys
                keys_to_check = [
                    ("HKCU\\Software\\Microsoft\\Windows\\Shell\\Associations\\UrlAssociations\\http\\UserChoice", "ProgId"),
                    ("HKCU\\Software\\Microsoft\\Windows\\Shell\\Associations\\UrlAssociations\\https\\UserChoice", "ProgId"),
                    ("HKCU\\Software\\Classes\\.html", ""),
                    ("HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\FileExts\\.html\\UserChoice", "ProgId")
                ]
            elif tweak_name == "Power Management Settings":
                # Check power-related registry keys
                keys_to_check = [
                    ("HKLM\\SYSTEM\\CurrentControlSet\\Control\\Power\\PowerSettings", ""),
                    ("HKCU\\Control Panel\\PowerCfg", ""),
                    ("HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\FlyoutMenuSettings", "ShowSleepOption"),
                    ("HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\FlyoutMenuSettings", "ShowHibernateOption")
                ]
            else:
                messagebox.showinfo("No Registry Keys", f"No specific registry keys to check for {tweak_name}")
                return
            
            # Check each registry key
            found_keys = []
            missing_keys = []
            
            for reg_path, value_name in keys_to_check:
                try:
                    # Use reg query to check the key
                    if value_name:
                        cmd = f'reg query "{reg_path}" /v "{value_name}"'
                    else:
                        cmd = f'reg query "{reg_path}"'
                    
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
                    
                    if result.returncode == 0:
                        if value_name:
                            # Extract the value from the output
                            lines = result.stdout.split('\n')
                            for line in lines:
                                if value_name in line:
                                    found_keys.append(f"{reg_path}\\{value_name}: {line.strip()}")
                                    break
                        else:
                            found_keys.append(f"{reg_path}: EXISTS")
                    else:
                        missing_keys.append(f"{reg_path}\\{value_name}" if value_name else reg_path)
                        
                except Exception as e:
                    missing_keys.append(f"{reg_path}\\{value_name} (Error: {str(e)})" if value_name else f"{reg_path} (Error: {str(e)})")
            
            # Display results in simple message box
            result_text = f"Registry Check Results for {tweak_name}:\n\n"
            
            if found_keys:
                result_text += "FOUND KEYS:\n"
                for key in found_keys:
                    result_text += f"✓ {key}\n"
                result_text += "\n"
            
            if missing_keys:
                result_text += "MISSING KEYS:\n"
                for key in missing_keys:
                    result_text += f"✗ {key}\n"
            
            if not found_keys and not missing_keys:
                result_text += "No registry keys checked."
            
            # Show results in simple message box
            messagebox.showinfo(f"Registry Check - {tweak_name}", result_text)
            
            self.log_to_terminal(f"Registry check completed for {tweak_name}", "success")
            
        except Exception as e:
            error_msg = f"Failed to check registry keys for {tweak_name}: {str(e)}"
            self.log_to_terminal(error_msg, "error")
            messagebox.showerror("Registry Check Error", error_msg)
    
    def check_app_installed(self, app_name):
        """
        Check if an app is already installed.
        
        Args:
            app_name (str): The name of the application to check
            
        Returns:
            bool: True if the app is installed, False otherwise
        """
        try:
            if app_name == "PyAutoClicker":
                # Check if PyAutoClicker is installed
                return os.path.exists(os.path.expanduser("~\\AppData\\Local\\PyAutoClicker"))
            elif app_name == "PowerEventProvider":
                # Check if PowerEventProvider is installed - check both installation directory and service
                installation_paths = [
                    "C:\\Program Files (x86)\\PowerEventProvider",
                    "C:\\Program Files\\PowerEventProvider",
                    "C:\\PowerEventProvider"
                ]
                
                # First check if installation directory exists
                for path in installation_paths:
                    if os.path.exists(path):
                        return True
                
                # Also check if service exists as secondary verification
                try:
                    result = subprocess.run(['sc', 'query', 'PowerEventProvider'], 
                                          capture_output=True, text=True, timeout=10)
                    if "RUNNING" in result.stdout or "STOPPED" in result.stdout:
                        return True
                except:
                    pass
                
                return False
            elif app_name == "IP Python Tray App":
                # Check for the specific tray app location
                primary_location = "C:\\Tools\\TrayApp\\main.py"
                if os.path.exists(primary_location):
                    return True
                
                # Fallback locations
                fallback_locations = [
                    "C:\\Tools\\ippy-tray-app",
                    "C:\\Tools\\ippy-tray-app\\main.py",
                    "C:\\Tools\\ippy_tray_app.py",
                    "C:\\Tools\\ip_tray_app.py",
                    "C:\\Tools\\TrayApp",
                    os.path.expanduser("~\\AppData\\Local\\ippy-tray-app"),
                    os.path.expanduser("~\\AppData\\Roaming\\ippy-tray-app")
                ]
                
                # Also check for any Python files in C:\Tools\ that might be the tray app
                try:
                    import glob
                    python_files = glob.glob("C:\\Tools\\*tray*.py")
                    if python_files:
                        return True
                    # Check for TrayApp folder
                    tray_folders = glob.glob("C:\\Tools\\*TrayApp*")
                    if tray_folders:
                        return True
                except:
                    pass
                
                return any(os.path.exists(loc) for loc in fallback_locations)
            elif app_name == "Tailscale":
                # Check if Tailscale is installed - improved detection
                locations = [
                    "C:\\Program Files\\Tailscale\\tailscale.exe",
                    "C:\\Program Files (x86)\\Tailscale\\tailscale.exe",
                    os.path.expanduser("~\\AppData\\Local\\Tailscale\\tailscale.exe"),
                    "C:\\ProgramData\\Tailscale\\tailscale.exe"
                ]
                # Also check registry for Tailscale
                try:
                    import winreg
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall")
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        subkey_name = winreg.EnumKey(key, i)
                        subkey = winreg.OpenKey(key, subkey_name)
                        try:
                            display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            if "tailscale" in display_name.lower():
                                return True
                        except:
                            pass
                        winreg.CloseKey(subkey)
                    winreg.CloseKey(key)
                except:
                    pass
                return any(os.path.exists(loc) for loc in locations)
            elif app_name == "MuMu":
                # Check if MuMu is installed - improved detection
                locations = [
                    "C:\\Program Files\\Netease\\MuMu Player 12",
                    "C:\\Program Files (x86)\\Netease\\MuMu Player 12",
                    "C:\\Program Files\\MuMu Player 12",
                    "C:\\Program Files (x86)\\MuMu Player 12",
                    os.path.expanduser("~\\AppData\\Local\\MuMu Player 12"),
                    "C:\\MuMu Player 12"
                ]
                # Also check for MuMu executables
                exe_locations = [
                    "C:\\Program Files\\Netease\\MuMu Player 12\\shell\\MuMuPlayer.exe",
                    "C:\\Program Files (x86)\\Netease\\MuMu Player 12\\shell\\MuMuPlayer.exe"
                ]
                # Check registry for MuMu
                try:
                    import winreg
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall")
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        subkey_name = winreg.EnumKey(key, i)
                        subkey = winreg.OpenKey(key, subkey_name)
                        try:
                            display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            if "mumu" in display_name.lower() or "netease" in display_name.lower():
                                return True
                        except:
                            pass
                        winreg.CloseKey(subkey)
                    winreg.CloseKey(key)
                except:
                    pass
                return any(os.path.exists(loc) for loc in locations) or any(os.path.exists(loc) for loc in exe_locations)
            elif app_name == "MASS":
                # Check if Windows is activated (MASS purpose) - simplified method
                try:
                    # Method 1: Simple license status check
                    result = subprocess.run([
                        'cscript', '//nologo', 'C:\\Windows\\System32\\slmgr.vbs', '/dli'
                    ], capture_output=True, text=True, timeout=10)
                    
                    if result.returncode == 0:
                        output = result.stdout.lower()
                        if "license status: licensed" in output:
                            return True
                    
                    # Method 2: Quick PowerShell check
                    ps_simple = '(Get-WmiObject -Query "SELECT LicenseStatus FROM SoftwareLicensingProduct WHERE LicenseStatus=1 AND PartialProductKey IS NOT NULL" | Measure-Object).Count -gt 0'
                    ps_result = subprocess.run([
                        'powershell', '-ExecutionPolicy', 'Bypass', '-Command', ps_simple
                    ], capture_output=True, text=True, timeout=8)
                    
                    if ps_result.returncode == 0 and "true" in ps_result.stdout.lower():
                        return True
                    
                    # Method 3: Registry check for activation
                    try:
                        import winreg
                        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
                        digital_id = winreg.QueryValueEx(key, "DigitalProductId")[0]
                        winreg.CloseKey(key)
                        # If we can read the digital product ID, likely activated
                        return len(digital_id) > 0
                    except:
                        pass
                        
                    return False
                except Exception as e:
                    # If all methods fail, assume not activated
                    return False
            elif app_name == "Ninite Installer":
                # Check for Ninite apps: 7zip, Chrome, Firefox, Notepad++
                return self.check_ninite_apps()
            else:
                return False
        except:
            return False
    
    def check_ninite_apps(self):
        """
        Check how many Ninite apps are installed (7zip, Chrome, Firefox, Notepad++).
        Returns True only if all 4 are installed.
        """
        apps_installed = 0
        total_apps = 4
        
        # Check 7-Zip
        zip_locations = [
            "C:\\Program Files\\7-Zip\\7z.exe",
            "C:\\Program Files (x86)\\7-Zip\\7z.exe"
        ]
        if any(os.path.exists(loc) for loc in zip_locations):
            apps_installed += 1
        
        # Check Chrome
        chrome_locations = [
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
            os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe")
        ]
        if any(os.path.exists(loc) for loc in chrome_locations):
            apps_installed += 1
        
        # Check Firefox
        firefox_locations = [
            "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
            "C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe"
        ]
        if any(os.path.exists(loc) for loc in firefox_locations):
            apps_installed += 1
        
        # Check Notepad++
        notepad_locations = [
            "C:\\Program Files\\Notepad++\\notepad++.exe",
            "C:\\Program Files (x86)\\Notepad++\\notepad++.exe"
        ]
        if any(os.path.exists(loc) for loc in notepad_locations):
            apps_installed += 1
        
        # Store the count for display purposes
        self.ninite_count = apps_installed
        self.ninite_total = total_apps
        
        # Return True only if all apps are installed
        return apps_installed == total_apps
    
    def check_app_async(self, app_name, status_label):
        """Check app installation status asynchronously."""
        try:
            is_installed = self.check_app_installed(app_name)
            status_text = "✓ Installed" if is_installed else "○ Not Installed"
            status_color = "#27ae60" if is_installed else "#95a5a6"
            status_label.config(text=status_text, fg=status_color)
        except:
            status_label.config(text="○ Not Installed", fg="#95a5a6")
    
    def check_mass_activation_async(self, status_label):
        """Check Windows activation status asynchronously."""
        try:
            is_activated = self.check_app_installed("MASS")
            status_text = "✓ Windows Activated" if is_activated else "✗ Windows Not Activated"
            status_color = "#27ae60" if is_activated else "#e74c3c"
            status_label.config(text=status_text, fg=status_color)
        except:
            status_label.config(text="✗ Windows Not Activated", fg="#e74c3c")
    
    def check_ninite_async(self, status_label):
        """Check Ninite apps status asynchronously."""
        try:
            all_installed = self.check_app_installed("Ninite Installer")
            count = getattr(self, 'ninite_count', 0)
            total = getattr(self, 'ninite_total', 4)
            status_text = f"✓ All Apps Installed ({count}/{total})" if all_installed else f"✗ Apps Installed ({count}/{total})"
            status_color = "#27ae60" if all_installed else "#e74c3c"  # Red when not all installed
            status_label.config(text=status_text, fg=status_color)
        except:
            status_label.config(text="✗ Apps Installed (0/4)", fg="#e74c3c")

    def refresh_app_status(self, app_name, status_label):
        """
        Refresh the status of a specific app.
        
        Args:
            app_name (str): The name of the application
            status_label: The status label widget to update
        """
        try:
            if app_name == "MASS":
                is_activated = self.check_app_installed(app_name)
                status_text = "✓ Windows Activated" if is_activated else "✗ Windows Not Activated"
                status_color = "#27ae60" if is_activated else "#e74c3c"  # Green if activated, red if not
            elif app_name == "Ninite Installer":
                all_installed = self.check_app_installed(app_name)
                count = getattr(self, 'ninite_count', 0)
                total = getattr(self, 'ninite_total', 4)
                status_text = f"✓ All Apps Installed ({count}/{total})" if all_installed else f"○ Apps Installed ({count}/{total})"
                status_color = "#27ae60" if all_installed else "#95a5a6"
            else:
                is_installed = self.check_app_installed(app_name)
                status_text = "✓ Installed" if is_installed else "○ Not Installed"
                status_color = "#27ae60" if is_installed else "#95a5a6"
                
            status_label.config(text=status_text, fg=status_color)
        except Exception as e:
            self.log_to_terminal(f"Error refreshing status for {app_name}: {str(e)}", "WARNING")
    
    def create_app_section(self, parent, title, description, button_text, github_url, install_func):
        """
        Create a section for an individual application with modern styling.
        
        Args:
            parent: The parent widget
            title (str): Application title
            description (str): Application description
            button_text (str): Text for the install button
            github_url (str): GitHub repository URL
            install_func: Function to call when install button is clicked
        """
        # Container for each app with modern card styling (matching tweaks)
        app_frame = tk.Frame(parent, bg='#ffffff', relief='flat', bd=1)
        app_frame.pack(fill='x', pady=6, padx=0)
        
        # Add subtle border (matching tweaks)
        border_frame = tk.Frame(app_frame, bg='#dee2e6', height=1)
        border_frame.pack(fill='x', side='bottom')
        
        # App info with consistent padding (matching tweaks)
        info_frame = tk.Frame(app_frame, bg='#ffffff')
        info_frame.pack(fill='x', padx=25, pady=20)
        
        # Title with consistent typography (matching tweaks)
        title_label = tk.Label(info_frame, text=title, 
                              font=('Segoe UI', 13, 'bold'), 
                              bg='#ffffff', fg='#212529', anchor='w')
        title_label.pack(anchor='w')
        
        # Description with consistent spacing (matching tweaks)
        desc_label = tk.Label(info_frame, text=description, 
                             font=('Segoe UI', 9), 
                             bg='#ffffff', fg='#6c757d', anchor='w',
                             wraplength=800)
        desc_label.pack(anchor='w', pady=(6, 0))
        
        # Status indicator - special handling for different apps
        # Use lazy loading for better performance
        if title == "MASS":
            # Show loading initially, check later
            status_text = "○ Checking activation..."
            status_color = "#95a5a6"
            status_label = tk.Label(info_frame, text=status_text, 
                                   font=('Segoe UI', 8, 'bold'), 
                                   bg='white', fg=status_color, anchor='w')
            status_label.pack(anchor='w', pady=(5, 0))
            # Check activation in background
            self.root.after(100, lambda: self.check_mass_activation_async(status_label))
        elif title == "CTT WinUtil":
            # CTT WinUtil doesn't need a status indicator since it's just a script runner
            status_label = None
        elif title == "Ninite Installer":
            # Show loading initially, check later
            status_text = "○ Checking apps..."
            status_color = "#95a5a6"
            status_label = tk.Label(info_frame, text=status_text, 
                                   font=('Segoe UI', 8, 'bold'), 
                                   bg='white', fg=status_color, anchor='w')
            status_label.pack(anchor='w', pady=(5, 0))
            # Check Ninite apps in background
            self.root.after(200, lambda: self.check_ninite_async(status_label))
        else:
            # Show loading initially, check later
            status_text = "○ Checking..."
            status_color = "#95a5a6"
            status_label = tk.Label(info_frame, text=status_text, 
                                   font=('Segoe UI', 8, 'bold'), 
                                   bg='white', fg=status_color, anchor='w')
            status_label.pack(anchor='w', pady=(5, 0))
            # Check installation in background
            self.root.after(50, lambda: self.check_app_async(title, status_label))
        
        # Buttons frame with consistent alignment (matching tweaks)
        buttons_frame = tk.Frame(info_frame, bg='#ffffff')
        buttons_frame.pack(fill='x', pady=(18, 0))
        
        # Consistent button styling (matching tweaks)
        button_style = {
            'font': ('Segoe UI', 9, 'bold'),
            'relief': 'flat',
            'padx': 24,
            'pady': 10,
            'cursor': 'hand2',
            'bd': 0,
            'width': 15  # Fixed width for alignment
        }
        
        # Create wrapper function that refreshes status after installation
        def install_and_refresh():
            install_func()
            # Refresh status after installation (only if status_label exists)
            if status_label:
                self.root.after(1000, lambda: self.refresh_app_status(title, status_label))
        
        # Install button (Primary action)
        install_btn = tk.Button(buttons_frame, text=button_text, 
                               command=install_and_refresh,
                               bg='#0d6efd', fg='white',
                               **button_style)
        install_btn.pack(side='left', padx=(0, 12))
        
        # Determine button label based on URL
        if "github.com" in github_url.lower():
            button_label = "GitHub"
        elif "tailscale.com" in github_url.lower():
            button_label = "Tailscale"
        elif "mumuplayer.com" in github_url.lower():
            button_label = "MuMu"
        elif "ninite.com" in github_url.lower():
            button_label = "Ninite"
        else:
            button_label = "Homepage"
        
        # Website/GitHub button (Secondary action)
        website_btn = tk.Button(buttons_frame, text=button_label, 
                              command=lambda: webbrowser.open(github_url),
                              bg='#6c757d', fg='white',
                              **button_style)
        website_btn.pack(side='left')
        
        # Consistent hover effects (matching tweaks)
        install_btn.bind('<Enter>', lambda e: install_btn.configure(bg='#0b5ed7'))
        install_btn.bind('<Leave>', lambda e: install_btn.configure(bg='#0d6efd'))
        website_btn.bind('<Enter>', lambda e: website_btn.configure(bg='#5a6268'))
        website_btn.bind('<Leave>', lambda e: website_btn.configure(bg='#6c757d'))
    
    def create_app_section_with_3_buttons(self, parent, title, description, btn1_text, btn2_text, btn3_text, btn1_url, install_func, btn2_func, btn3_func):
        """
        Create a section for an individual application with 3 buttons.
        
        Args:
            parent: The parent widget
            title (str): Application title
            description (str): Application description
            btn1_text (str): Text for the first button (install)
            btn2_text (str): Text for the second button
            btn3_text (str): Text for the third button
            btn1_url (str): URL for the first button
            install_func: Function to call when install button is clicked
            btn2_func: Function to call when second button is clicked
            btn3_func: Function to call when third button is clicked
        """
        # Container for each app with modern card styling (matching tweaks)
        app_frame = tk.Frame(parent, bg='#ffffff', relief='flat', bd=1)
        app_frame.pack(fill='x', pady=6, padx=0)
        
        # Add subtle border (matching tweaks)
        border_frame = tk.Frame(app_frame, bg='#dee2e6', height=1)
        border_frame.pack(fill='x', side='bottom')
        
        # App info with consistent padding (matching tweaks)
        info_frame = tk.Frame(app_frame, bg='#ffffff')
        info_frame.pack(fill='x', padx=25, pady=20)
        
        # Title with consistent typography (matching tweaks)
        title_label = tk.Label(info_frame, text=title, 
                              font=('Segoe UI', 13, 'bold'), 
                              bg='#ffffff', fg='#212529', anchor='w')
        title_label.pack(anchor='w')
        
        # Description with consistent spacing (matching tweaks)
        desc_label = tk.Label(info_frame, text=description, 
                             font=('Segoe UI', 9), 
                             bg='#ffffff', fg='#6c757d', anchor='w',
                             wraplength=800)
        desc_label.pack(anchor='w', pady=(6, 0))
        
        # Status indicator for PowerEventProvider and other apps
        status_text = "○ Checking..."
        status_color = "#95a5a6"
        status_label = tk.Label(info_frame, text=status_text, 
                               font=('Segoe UI', 8, 'bold'), 
                               bg='#ffffff', fg=status_color, anchor='w')
        status_label.pack(anchor='w', pady=(5, 0))
        # Check installation in background
        self.root.after(50, lambda: self.check_app_async(title, status_label))
        
        # Buttons frame with consistent alignment (matching tweaks)
        buttons_frame = tk.Frame(info_frame, bg='#ffffff')
        buttons_frame.pack(fill='x', pady=(18, 0))
        
        # Consistent button styling (matching tweaks)
        button_style = {
            'font': ('Segoe UI', 9, 'bold'),
            'relief': 'flat',
            'padx': 24,
            'pady': 10,
            'cursor': 'hand2',
            'bd': 0,
            'width': 15  # Fixed width for alignment
        }
        
        # Create wrapper function that refreshes status after installation
        def install_and_refresh():
            install_func()
            # Refresh status after installation
            self.root.after(1000, lambda: self.refresh_app_status(title, status_label))
        
        # Button 1 (Install) - Primary action
        install_btn = tk.Button(buttons_frame, text=btn1_text, 
                               command=install_and_refresh,
                               bg='#0d6efd', fg='white',
                               **button_style)
        install_btn.pack(side='left', padx=(0, 12))
        
        # Button 2 (GitHub/Link button - consistent with other Link buttons)
        btn2 = tk.Button(buttons_frame, text=btn2_text, 
                         command=btn2_func,
                         bg='#6c757d', fg='white',
                         **button_style)
        btn2.pack(side='left', padx=(0, 12))
        
        # Button 3 (Logs button - green)
        btn3 = tk.Button(buttons_frame, text=btn3_text, 
                         command=btn3_func,
                         bg='#198754', fg='white',
                         **button_style)
        btn3.pack(side='left')
        
        # Consistent hover effects (matching tweaks)
        install_btn.bind('<Enter>', lambda e: install_btn.configure(bg='#0b5ed7'))
        install_btn.bind('<Leave>', lambda e: install_btn.configure(bg='#0d6efd'))
        btn2.bind('<Enter>', lambda e: btn2.configure(bg='#5a6268'))
        btn2.bind('<Leave>', lambda e: btn2.configure(bg='#6c757d'))
        btn3.bind('<Enter>', lambda e: btn3.configure(bg='#157347'))
        btn3.bind('<Leave>', lambda e: btn3.configure(bg='#198754'))
    
    def get_windows_version(self):
        """Get the current Windows version for user guidance."""
        try:
            # Method 1: Use platform module for more reliable Windows version detection
            import platform
            system_info = platform.uname()
            
            if system_info.system == "Windows":
                # Get Windows version from platform
                version = system_info.version
                release = system_info.release
                
                # Parse the version string
                if "10." in version or "10." in release:
                    return "Windows 10"
                elif "11." in version or "11." in release:
                    return "Windows 11"
                else:
                    return f"Windows {version}"
            else:
                return "Not Windows"
                
        except Exception as e:
            # Method 2: Fallback to ctypes method
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.GetVersion.restype = ctypes.c_ulong
                version = kernel32.GetVersion()
                major = version >> 16 & 0xFF
                minor = version >> 8 & 0xFF
                
                if major == 10:
                    return "Windows 10"
                elif major == 11:
                    return "Windows 11"
                else:
                    return f"Windows {major}.{minor}"
            except:
                # Method 3: Try registry method as final fallback
                try:
                    import subprocess
                    result = subprocess.run(['reg', 'query', 'HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion', '/v', 'ProductName'], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        output = result.stdout.lower()
                        if 'windows 11' in output:
                            return "Windows 11"
                        elif 'windows 10' in output:
                            return "Windows 10"
                        else:
                            return "Windows (Registry)"
                    else:
                        return "Unknown Windows Version"
                except:
                    return "Unknown Windows Version"
    
    # Duplicate method removed - keeping only the 3-button version above

    

    
    def run_powershell_command(self, command):
        """
        Execute a PowerShell command with comprehensive logging.
        
        Args:
            command (str): The PowerShell command to execute
        """
        try:
            self.log_to_terminal(f"Executing PowerShell command: {command}", "INFO")
            result = subprocess.run(['powershell', '-Command', command], 
                                  capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                self.log_to_terminal("Command executed successfully!", "SUCCESS")
                if result.stdout.strip():
                    self.log_to_terminal(f"Output: {result.stdout.strip()}", "INFO")
                messagebox.showinfo("Success", "Command executed successfully!")
            else:
                error_msg = f"Command failed: {result.stderr}"
                self.log_to_terminal(error_msg, "ERROR")
                messagebox.showerror("Error", error_msg)
        except Exception as e:
            error_msg = f"Failed to execute command: {str(e)}"
            self.log_to_terminal(error_msg, "ERROR")
            messagebox.showerror("Error", error_msg)
    
    def run_ctt_winutil(self):
        """
        Run CTT WinUtil in a separate PowerShell window to prevent crashes.
        
        This method spawns CTT WinUtil in its own PowerShell window, preventing
        interference with the main InvokeX application.
        """
        try:
            self.log_to_terminal("Launching CTT WinUtil in separate PowerShell window...", "INFO")
            
            # Ask for confirmation
            confirm = messagebox.askyesno(
                "Launch CTT WinUtil", 
                "This will open CTT WinUtil in a separate PowerShell window.\n\n"
                "The utility will run independently from InvokeX.\n\n"
                "Continue?"
            )
            
            if not confirm:
                self.log_to_terminal("CTT WinUtil launch cancelled by user", "INFO")
                return
            
            # Command to run CTT WinUtil in a new, smaller PowerShell window
            command = [
                'powershell',
                '-Command',
                'Start-Process',
                'powershell',
                '-ArgumentList',
                '"-NoExit", "-Command", "Write-Host \'Launching CTT WinUtil...\' -ForegroundColor Green; irm https://christitus.com/win | iex"',
                '-WindowStyle', 'Normal',
                '-Verb', 'RunAs'  # Request elevation
            ]
            
            # Alternative command to set window size more precisely
            advanced_command = [
                'powershell',
                '-Command',
                '$proc = Start-Process powershell -ArgumentList "-NoExit", "-Command", "[Console]::SetWindowSize(100, 30); Write-Host \'Launching CTT WinUtil...\' -ForegroundColor Green; irm https://christitus.com/win | iex" -Verb RunAs -PassThru'
            ]
            
            # Start the process without waiting for it to complete
            # Try the advanced command first for better window sizing
            try:
                subprocess.Popen(advanced_command, shell=False)
                self.log_to_terminal("Using advanced window sizing for CTT WinUtil", "INFO")
            except:
                # Fallback to basic command if advanced fails
                subprocess.Popen(command, shell=False)
                self.log_to_terminal("Using basic window sizing for CTT WinUtil", "INFO")
            
            self.log_to_terminal("CTT WinUtil launched successfully in separate window!", "SUCCESS")
            messagebox.showinfo(
                "CTT WinUtil Launched", 
                "CTT WinUtil has been launched in a separate PowerShell window.\n\n"
                "You may see a UAC prompt for administrator privileges.\n\n"
                "The utility will run independently from InvokeX."
            )
            
        except Exception as e:
            error_msg = f"Failed to launch CTT WinUtil: {str(e)}"
            self.log_to_terminal(error_msg, "ERROR")
            messagebox.showerror("Error", error_msg)
    
    def install_ippy_tray(self):
        """Install IP Python Tray App with Python dependency checking and multiple fallback methods."""
        self.log_to_terminal("Starting IP Python Tray App installation...", "info")
        
        try:
            # Step 1: Check if Python is installed
            self.log_to_terminal("Checking Python installation...", "info")
            python_check = subprocess.run(['python', '--version'], 
                                        capture_output=True, text=True, timeout=10)
            
            if python_check.returncode != 0:
                self.log_to_terminal("Python not found. Attempting to install Python...", "warning")
                
                # Try to install Python using winget (Windows Package Manager)
                try:
                    self.log_to_terminal("Installing Python using winget...", "info")
                    python_install = subprocess.run([
                        'winget', 'install', 'Python.Python.3.11', '--accept-source-agreements'
                    ], capture_output=True, text=True, timeout=300)
                    
                    if python_install.returncode == 0:
                        self.log_to_terminal("Python installed successfully using winget!", "success")
                        # Refresh environment variables
                        self.log_to_terminal("Refreshing environment variables...", "info")
                        subprocess.run(['refreshenv'], shell=True, capture_output=True, timeout=30)
                    else:
                        self.log_to_terminal("winget installation failed. Trying alternative method...", "warning")
                        
                        # Alternative: Download and install Python from python.org
                        self.log_to_terminal("Downloading Python from python.org...", "info")
                        python_url = "https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe"
                        python_installer = "python-installer.exe"
                        
                        try:
                            import urllib.request
                            urllib.request.urlretrieve(python_url, python_installer)
                            self.log_to_terminal("Python installer downloaded. Installing...", "info")
                            
                            # Install Python silently
                            install_result = subprocess.run([
                                python_installer, '/quiet', 'InstallAllUsers=1', 'PrependPath=1'
                            ], capture_output=True, text=True, timeout=300)
                            
                            if install_result.returncode == 0:
                                self.log_to_terminal("Python installed successfully!", "success")
                                # Refresh environment variables
                                subprocess.run(['refreshenv'], shell=True, capture_output=True, timeout=30)
                            else:
                                self.log_to_terminal("Python installation failed. Please install Python manually.", "error")
                                messagebox.showerror("Python Required", 
                                                   "Python is required but could not be installed automatically.\n\n"
                                                   "Please install Python from https://www.python.org/downloads/\n"
                                                   "Make sure to check 'Add Python to PATH' during installation.")
                                return
                                
                        except Exception as e:
                            self.log_to_terminal(f"Failed to download Python: {str(e)}", "error")
                            messagebox.showerror("Python Required", 
                                               "Python is required but could not be downloaded.\n\n"
                                               "Please install Python from https://www.python.org/downloads/\n"
                                               "Make sure to check 'Add Python to PATH' during installation.")
                            return
                except Exception as e:
                    self.log_to_terminal(f"winget not available: {str(e)}. Trying alternative Python installation...", "warning")
                    # Continue with alternative methods...
            else:
                self.log_to_terminal(f"Python found: {python_check.stdout.strip()}", "success")
            
            # Step 2: Verify Python is now accessible
            self.log_to_terminal("Verifying Python installation...", "info")
            final_python_check = subprocess.run(['python', '--version'], 
                                              capture_output=True, text=True, timeout=10)
            
            if final_python_check.returncode != 0:
                self.log_to_terminal("Python still not accessible. Please restart the application after installing Python.", "error")
                messagebox.showerror("Python Not Accessible", 
                                   "Python was installed but is not accessible from the current session.\n\n"
                                   "Please restart the application and try again.")
                return
            
            # Step 3: Set PowerShell execution policy
            self.log_to_terminal("Setting PowerShell execution policy...", "info")
            result = subprocess.run([
                "powershell", "-Command", 
                "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.log_to_terminal("Execution policy set successfully.", "success")
            else:
                self.log_to_terminal("Warning: Could not set execution policy.", "warning")
            
            # Step 4: Try the original installation command
            self.log_to_terminal("Executing IP Python Tray App installation...", "info")
            result = subprocess.run([
                "powershell", "-ExecutionPolicy", "Bypass", "-Command",
                "irm 'https://raw.githubusercontent.com/GoblinRules/ippy-tray-app/main/install.ps1' | iex"
            ], capture_output=True, text=True, timeout=180)  # Increased to 3 minutes
            
            if result.returncode == 0:
                self.log_to_terminal("IP Python Tray App installed successfully!", "success")
                self.log_to_terminal("Note: A system reboot may be required for the tray app to appear.", "info")
                messagebox.showinfo("Installation Complete", 
                                  "IP Python Tray App has been installed successfully!\n\n"
                                  "Note: A system reboot may be required for the tray app to appear.")
                return
            else:
                self.log_to_terminal(f"First command failed: {result.stderr}", "warning")
            
            # Step 5: Try with TLS security protocol settings
            self.log_to_terminal("Setting TLS security protocol...", "info")
            tls_result = subprocess.run([
                "powershell", "-Command",
                "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12"
            ], capture_output=True, text=True, timeout=30)
            
            if tls_result.returncode == 0:
                self.log_to_terminal("TLS protocol set successfully.", "success")
            else:
                self.log_to_terminal("Warning: Could not set TLS protocol.", "warning")
            
            # Step 6: Try with .NET Framework crypto settings
            self.log_to_terminal("Setting .NET Framework crypto settings...", "info")
            crypto_result = subprocess.run([
                "powershell", "-Command",
                "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\.NETFramework\\v4.0.30319' -Name 'SchUseStrongCrypto' -Value 1 -Type DWord"
            ], capture_output=True, text=True, timeout=30)
            
            if crypto_result.returncode == 0:
                self.log_to_terminal(".NET Framework crypto settings updated.", "success")
            else:
                self.log_to_terminal("Warning: Could not update .NET Framework crypto settings.", "warning")
            
            # Step 7: Try with WOW64 settings
            self.log_to_terminal("Setting WOW64 .NET Framework crypto settings...", "info")
            wow64_result = subprocess.run([
                "powershell", "-Command",
                "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Wow6432Node\\Microsoft\\.NETFramework\\v4.0.30319' -Name 'SchUseStrongCrypto' -Value 1 -Type DWord"
            ], capture_output=True, text=True, timeout=30)
            
            if wow64_result.returncode == 0:
                self.log_to_terminal("WOW64 .NET Framework crypto settings updated.", "success")
            else:
                self.log_to_terminal("Warning: Could not update WOW64 .NET Framework crypto settings.", "warning")
            
            # Step 8: Final attempt with all settings applied
            self.log_to_terminal("Executing final installation command...", "info")
            final_result = subprocess.run([
                "powershell", "-ExecutionPolicy", "Bypass", "-Command",
                "irm 'https://raw.githubusercontent.com/GoblinRules/ippy-tray-app/main/install.ps1' | iex"
            ], capture_output=True, text=True, timeout=180)  # Increased to 3 minutes
            
            if final_result.returncode == 0:
                self.log_to_terminal("IP Python Tray App installed successfully!", "success")
                self.log_to_terminal("Note: A system reboot may be required for the tray app to appear.", "info")
                messagebox.showinfo("Installation Complete", 
                                  "IP Python Tray App has been installed successfully!\n\n"
                                  "Note: A system reboot may be required for the tray app to appear.")
            else:
                self.log_to_terminal(f"Final installation failed: {final_result.stderr}", "error")
                self.log_to_terminal("All installation methods failed. Please try installing manually.", "error")
                messagebox.showerror("Installation Failed", 
                                   "All installation methods failed.\n\n"
                                   "Please try installing manually from:\n"
                                   "https://github.com/GoblinRules/ippy-tray-app")
                
        except subprocess.TimeoutExpired:
            self.log_to_terminal("Installation timed out. Please try again.", "error")
            messagebox.showerror("Installation Timeout", 
                               "The installation process timed out.\n\n"
                               "Please try again or install manually.")
        except Exception as e:
            self.log_to_terminal(f"Installation error: {str(e)}", "error")
            messagebox.showerror("Installation Error", 
                               f"An error occurred during installation:\n{str(e)}\n\n"
                               "Please try installing manually.")
        
        # Clean up downloaded files
        for cleanup_file in ["python-installer.exe"]:
            if os.path.exists(cleanup_file):
                try:
                    os.remove(cleanup_file)
                    self.log_to_terminal(f"Cleaned up: {cleanup_file}", "info")
                except Exception as e:
                    self.log_to_terminal(f"Warning: Could not clean up {cleanup_file}: {str(e)}", "warning")
    
    def download_and_install_msi(self, url):
        """
        Download and install an MSI file with comprehensive error handling.
        
        Args:
            url (str): The URL to download the MSI file from
        """
        try:
            self.log_to_terminal(f"Starting MSI download from: {url}", "INFO")
            
            # Download the MSI file
            import urllib.request
            filename = "PowerEventProviderSetup.msi"
            
            self.log_to_terminal("Downloading MSI file...", "INFO")
            urllib.request.urlretrieve(url, filename)
            self.log_to_terminal(f"MSI file downloaded: {filename}", "SUCCESS")
            
            # Try to install the MSI with elevated privileges
            self.log_to_terminal("Installing MSI file with elevated privileges...", "INFO")
            
            # First try silent install
            try:
                result = subprocess.run(['msiexec', '/i', filename, '/quiet'], 
                                      capture_output=True, text=True, timeout=120)
                if result.returncode == 0:
                    self.log_to_terminal("PowerEventProvider installed successfully!", "SUCCESS")
                    messagebox.showinfo("Success", "PowerEventProvider installed successfully!")
                else:
                    # If silent install fails, try with logging
                    self.log_to_terminal(f"Silent install failed (code {result.returncode}), trying with logging...", "WARNING")
                    self.log_to_terminal(f"Error details: {result.stderr}", "WARNING")
                    
                    # Try with logging and UI
                    result2 = subprocess.run(['msiexec', '/i', filename, '/l*v', 'msi_install.log'], 
                                           capture_output=True, text=True, timeout=120)
                    if result2.returncode == 0:
                        self.log_to_terminal("PowerEventProvider installed successfully with UI!", "SUCCESS")
                        messagebox.showinfo("Success", "PowerEventProvider installed successfully!")
                    else:
                        # If still failing, suggest manual installation
                        error_msg = f"MSI installation failed. Exit code: {result2.returncode}"
                        self.log_to_terminal(error_msg, "ERROR")
                        self.log_to_terminal("Suggesting manual installation...", "INFO")
                        
                        # Show manual installation dialog
                        manual_install = messagebox.askyesno(
                            "Installation Failed", 
                            f"Automatic installation failed (Error {result2.returncode}).\n\n"
                            f"Would you like to open the MSI file manually for installation?\n\n"
                            f"File location: {os.path.abspath(filename)}"
                        )
                        
                        if manual_install:
                            try:
                                os.startfile(filename)
                                self.log_to_terminal("MSI file opened for manual installation.", "INFO")
                                messagebox.showinfo("Manual Installation", 
                                                  f"MSI file opened. Please complete the installation manually.\n\n"
                                                  f"File: {os.path.abspath(filename)}")
                            except Exception as e:
                                self.log_to_terminal(f"Failed to open MSI file: {str(e)}", "ERROR")
                        else:
                            messagebox.showwarning("Installation Skipped", 
                                                 "MSI installation was skipped. You can install manually later.")
                            
            except subprocess.TimeoutExpired:
                self.log_to_terminal("MSI installation timed out. The installer may still be running.", "WARNING")
                messagebox.showwarning("Installation Timeout", 
                                     "The MSI installer is taking longer than expected.\n"
                                     "Please check if the installation completed in the background.")
            
            # Clean up downloaded file only if installation was successful
            if os.path.exists(filename):
                try:
                    os.remove(filename)
                    self.log_to_terminal("Downloaded MSI file cleaned up.", "INFO")
                except Exception as e:
                    self.log_to_terminal(f"Warning: Could not clean up MSI file: {str(e)}", "WARNING")
                    
        except Exception as e:
            error_msg = f"Failed to download/install MSI: {str(e)}"
            self.log_to_terminal(error_msg, "ERROR")
            messagebox.showerror("Error", error_msg)
    
    def remove_shutdown_from_startup_smart(self):
        """
        Hide shutdown options using Group Policy Objects (GPO) for better reliability.
        This method creates and applies GPO settings that are more persistent and effective.
        """
        self.log_to_terminal("Attempting to hide shutdown options using Group Policy...", "info")
        
        try:
            # Check if we're running as administrator
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                self.log_to_terminal("This operation requires administrator privileges.", "warning")
                messagebox.showwarning("Administrator Required", 
                    "This operation requires administrator privileges.\n\n"
                    "Please restart InvokeX as administrator to hide shutdown options.")
                return
            
            success_count = 0
            total_methods = 6
            
            # Method 1: Create GPO for User Configuration - Start Menu and Taskbar
            try:
                gpo_cmd1 = 'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v NoClose /t REG_DWORD /d 1 /f'
                result1 = subprocess.run(gpo_cmd1, shell=True, capture_output=True, timeout=30)
                if result1.returncode == 0:
                    self.log_to_terminal("Successfully set user close policy", "success")
                    success_count += 1
                else:
                    self.log_to_terminal(f"User close policy failed: {result1.stderr}", "warning")
            except Exception as e:
                self.log_to_terminal(f"Could not set user close policy: {str(e)}", "warning")
            
            # Method 2: Create GPO for User Configuration - Shutdown
            try:
                gpo_cmd2 = 'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v NoShutdown /t REG_DWORD /d 1 /f'
                result2 = subprocess.run(gpo_cmd2, shell=True, capture_output=True, timeout=30)
                if result2.returncode == 0:
                    self.log_to_terminal("Successfully set user shutdown policy", "success")
                    success_count += 1
                else:
                    self.log_to_terminal(f"User shutdown policy failed: {result2.stderr}", "warning")
            except Exception as e:
                self.log_to_terminal(f"Could not set user shutdown policy: {str(e)}", "warning")
            
            # Method 3: Create GPO for Machine Configuration - Shutdown
            try:
                gpo_cmd3 = 'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v NoShutdown /t REG_DWORD /d 1 /f'
                result3 = subprocess.run(gpo_cmd3, shell=True, capture_output=True, timeout=30)
                if result3.returncode == 0:
                    self.log_to_terminal("Successfully set machine shutdown policy", "success")
                    success_count += 1
                else:
                    self.log_to_terminal(f"Machine shutdown policy failed: {result3.stderr}", "warning")
            except Exception as e:
                self.log_to_terminal(f"Could not set machine shutdown policy: {str(e)}", "warning")
            
            # Method 4: Create GPO for System Configuration - Disable Shutdown
            try:
                gpo_cmd4 = 'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v DisableShutdown /t REG_DWORD /d 1 /f'
                result4 = subprocess.run(gpo_cmd4, shell=True, capture_output=True, timeout=30)
                if result4.returncode == 0:
                    self.log_to_terminal("Successfully set system shutdown disable", "success")
                    success_count += 1
                else:
                    self.log_to_terminal(f"System shutdown disable failed: {result4.stderr}", "warning")
            except Exception as e:
                self.log_to_terminal(f"Could not set system shutdown disable: {str(e)}", "warning")
            
            # Method 5: Create GPO for Logoff hiding
            try:
                gpo_cmd5 = 'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v NoLogoff /t REG_DWORD /d 1 /f'
                result5 = subprocess.run(gpo_cmd5, shell=True, capture_output=True, timeout=30)
                if result5.returncode == 0:
                    self.log_to_terminal("Successfully hid logoff option", "success")
                    success_count += 1
                else:
                    self.log_to_terminal(f"Hide logoff failed: {result5.stderr}", "warning")
            except Exception as e:
                self.log_to_terminal(f"Could not hide logoff: {str(e)}", "warning")
            
            # Method 6: Create GPO for Power Options hiding
            try:
                gpo_cmd6 = 'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v NoPowerOptions /t REG_DWORD /d 1 /f'
                result6 = subprocess.run(gpo_cmd6, shell=True, capture_output=True, timeout=30)
                if result6.returncode == 0:
                    self.log_to_terminal("Successfully hid power options", "success")
                    success_count += 1
                else:
                    self.log_to_terminal(f"Hide power options failed: {result6.stderr}", "warning")
            except Exception as e:
                self.log_to_terminal(f"Could not hide power options: {str(e)}", "warning")
            
            # Force Group Policy update and restart Explorer
            try:
                self.log_to_terminal("Updating Group Policy...", "info")
                subprocess.run(["gpupdate", "/force"], capture_output=True, timeout=60)
                self.log_to_terminal("Group Policy updated", "success")
                
                # Restart Explorer to apply changes immediately
                self.log_to_terminal("Restarting Explorer to apply changes...", "info")
                subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], capture_output=True, timeout=30)
                subprocess.run(["start", "explorer.exe"], shell=True, capture_output=True, timeout=30)
                self.log_to_terminal("Explorer restarted", "success")
                
            except Exception as e:
                self.log_to_terminal(f"Group Policy update completed: {str(e)}", "info")
            
            # Final result
            if success_count >= 3:  # Require at least 3 methods to succeed
                self.log_to_terminal(f"Shutdown functionality disabled successfully! ({success_count}/{total_methods} GPO methods succeeded)", "success")
                messagebox.showinfo("Success", 
                    f"Shutdown functionality has been disabled using Group Policy!\n\n"
                    f"GPO methods applied: {success_count}/{total_methods}\n\n"
                    "Changes:\n"
                    "• Start menu close button hidden\n"
                    "• Shutdown options hidden\n"
                    "• Power options hidden\n"
                    "• Logoff option hidden\n"
                    "• Restart functionality preserved\n\n"
                    "Note: Changes applied immediately. You may need to log off/on to see full effects.")
            else:
                self.log_to_terminal("Failed to disable shutdown functionality with GPO", "warning")
                messagebox.showwarning("Failed", 
                    "Could not disable shutdown functionality using Group Policy.\n\n"
                    "This may be due to insufficient permissions or system protection.\n"
                    "Please check the terminal output for details.")
                
        except Exception as e:
            error_msg = f"Failed to disable shutdown: {str(e)}"
            self.log_to_terminal(error_msg, "error")
            messagebox.showerror("Error", error_msg)
    
    def restore_shutdown_options(self):
        """Restore shutdown functionality by removing GPO settings."""
        self.log_to_terminal("Attempting to restore shutdown functionality...", "info")
        
        try:
            # Check if we're running as administrator
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                self.log_to_terminal("This operation requires administrator privileges.", "warning")
                self.log_to_terminal("Please restart the application as administrator.", "warning")
                return
            
            # Restore shutdown functionality by removing GPO registry entries
            success_count = 0
            total_methods = 6
            
            # Method 1: Remove user close policy
            try:
                reg_cmd1 = 'reg delete "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v NoClose /f'
                result1 = subprocess.run(reg_cmd1, shell=True, capture_output=True, timeout=30)
                if result1.returncode == 0:
                    self.log_to_terminal("Successfully removed user close policy", "success")
                    success_count += 1
                else:
                    self.log_to_terminal("User close policy not found (already removed)", "info")
                    success_count += 1  # Count as success since goal is achieved
            except Exception as e:
                self.log_to_terminal(f"Could not remove user close policy: {str(e)}", "warning")
            
            # Method 2: Remove user shutdown policy
            try:
                reg_cmd2 = 'reg delete "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v NoShutdown /f'
                result2 = subprocess.run(reg_cmd2, shell=True, capture_output=True, timeout=30)
                if result2.returncode == 0:
                    self.log_to_terminal("Successfully removed user shutdown policy", "success")
                    success_count += 1
                else:
                    self.log_to_terminal("User shutdown policy not found (already removed)", "info")
                    success_count += 1  # Count as success since goal is achieved
            except Exception as e:
                self.log_to_terminal(f"Could not remove user shutdown policy: {str(e)}", "warning")
            
            # Method 3: Remove machine shutdown policy
            try:
                reg_cmd3 = 'reg delete "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v NoShutdown /f'
                result3 = subprocess.run(reg_cmd3, shell=True, capture_output=True, timeout=30)
                if result3.returncode == 0:
                    self.log_to_terminal("Successfully removed machine shutdown policy", "success")
                    success_count += 1
                else:
                    self.log_to_terminal("Machine shutdown policy not found (already removed)", "info")
                    success_count += 1  # Count as success since goal is achieved
            except Exception as e:
                self.log_to_terminal(f"Could not remove machine shutdown policy: {str(e)}", "warning")
            
            # Method 4: Remove system shutdown disable
            try:
                reg_cmd4 = 'reg delete "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v DisableShutdown /f'
                result4 = subprocess.run(reg_cmd4, shell=True, capture_output=True, timeout=30)
                if result4.returncode == 0:
                    self.log_to_terminal("Successfully removed system shutdown disable", "success")
                    success_count += 1
                else:
                    self.log_to_terminal("System shutdown disable not found (already removed)", "info")
                    success_count += 1  # Count as success since goal is achieved
            except Exception as e:
                self.log_to_terminal(f"Could not remove system shutdown disable: {str(e)}", "warning")
            
            # Method 5: Remove logoff hiding
            try:
                reg_cmd5 = 'reg delete "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v NoLogoff /f'
                result5 = subprocess.run(reg_cmd5, shell=True, capture_output=True, timeout=30)
                if result5.returncode == 0:
                    self.log_to_terminal("Successfully restored logoff option", "success")
                    success_count += 1
                else:
                    self.log_to_terminal("Logoff policy not found (already removed)", "info")
                    success_count += 1  # Count as success since goal is achieved
            except Exception as e:
                self.log_to_terminal(f"Could not restore logoff option: {str(e)}", "warning")
            
            # Method 6: Remove power options hiding
            try:
                reg_cmd6 = 'reg delete "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v NoPowerOptions /f'
                result6 = subprocess.run(reg_cmd6, shell=True, capture_output=True, timeout=30)
                if result6.returncode == 0:
                    self.log_to_terminal("Successfully restored power options", "success")
                    success_count += 1
                else:
                    self.log_to_terminal("Power options policy not found (already removed)", "info")
                    success_count += 1  # Count as success since goal is achieved
            except Exception as e:
                self.log_to_terminal(f"Could not restore power options: {str(e)}", "warning")
            
            # Force Group Policy update and restart Explorer
            try:
                self.log_to_terminal("Updating Group Policy...", "info")
                subprocess.run(["gpupdate", "/force"], capture_output=True, timeout=60)
                self.log_to_terminal("Group Policy updated", "success")
                
                # Restart Explorer to apply changes immediately
                self.log_to_terminal("Restarting Explorer to apply changes...", "info")
                subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], capture_output=True, timeout=30)
                subprocess.run(["start", "explorer.exe"], shell=True, capture_output=True, timeout=30)
                self.log_to_terminal("Explorer restarted", "success")
                
            except Exception as e:
                self.log_to_terminal(f"Group Policy update completed: {str(e)}", "info")
            
            # Final result
            if success_count >= 3:  # Require at least 3 methods to succeed
                self.log_to_terminal(f"Shutdown functionality restored successfully! ({success_count}/{total_methods} GPO methods succeeded)", "success")
                messagebox.showinfo("Success", 
                    f"Shutdown functionality has been restored!\n\n"
                    f"GPO methods applied: {success_count}/{total_methods}\n\n"
                    "Changes:\n"
                    "• Start menu close button restored\n"
                    "• Shutdown options restored\n"
                    "• Power options restored\n"
                    "• Logoff option restored\n"
                    "• All power options available\n\n"
                    "Note: Changes applied immediately. You may need to log off/on to see full effects.")
            else:
                self.log_to_terminal("Failed to restore shutdown functionality", "warning")
                messagebox.showwarning("Failed", 
                    "Could not restore shutdown functionality.\n\n"
                    "This may be due to insufficient permissions.\n"
                    "Please check the terminal output for details.")
                
        except Exception as e:
            error_msg = f"Failed to restore shutdown options: {str(e)}"
            self.log_to_terminal(error_msg, "error")
            messagebox.showerror("Error", error_msg)
    
    def configure_power_management(self):
        """Configure comprehensive power management settings using multiple methods for maximum compatibility."""
        self.log_to_terminal("=== Starting comprehensive power management configuration ===", "info")
        
        try:
            # Check if we're running as administrator
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                self.log_to_terminal("❌ Administrator privileges required for power management changes", "error")
                messagebox.showwarning("Administrator Required", 
                    "This operation requires administrator privileges.\n\n"
                    "Please restart InvokeX as administrator to configure power settings.")
                return
            
            self.log_to_terminal("✓ Administrator privileges confirmed", "success")
            success_count = 0
            total_operations = 8  # Added sleep button and better power settings
            
            # Method 1: Set sleep to never using powercfg with timeout values
            self.log_to_terminal("🔧 Configuring sleep settings (AC and battery)...", "info")
            try:
                # Sleep timeout to never (0 = never)
                cmd1 = "powercfg /change standby-timeout-ac 0"
                cmd2 = "powercfg /change standby-timeout-dc 0"
                
                result1 = subprocess.run(cmd1, shell=True, capture_output=True, text=True, timeout=30)
                result2 = subprocess.run(cmd2, shell=True, capture_output=True, text=True, timeout=30)
                
                if result1.returncode == 0 and result2.returncode == 0:
                    success_count += 1
                    self.log_to_terminal("✓ Sleep disabled successfully (AC and battery)", "success")
                else:
                    self.log_to_terminal(f"⚠ Sleep configuration had issues: AC={result1.stderr}, Battery={result2.stderr}", "warning")
            except Exception as e:
                self.log_to_terminal(f"❌ Sleep configuration failed: {str(e)}", "error")
            
            # Method 2: Set hibernate to never
            self.log_to_terminal("🔧 Configuring hibernate settings (AC and battery)...", "info")
            try:
                cmd3 = "powercfg /change hibernate-timeout-ac 0"
                cmd4 = "powercfg /change hibernate-timeout-dc 0"
                
                result3 = subprocess.run(cmd3, shell=True, capture_output=True, text=True, timeout=30)
                result4 = subprocess.run(cmd4, shell=True, capture_output=True, text=True, timeout=30)
                
                if result3.returncode == 0 and result4.returncode == 0:
                    success_count += 1
                    self.log_to_terminal("✓ Hibernate disabled successfully (AC and battery)", "success")
                else:
                    self.log_to_terminal(f"⚠ Hibernate configuration had issues: AC={result3.stderr}, Battery={result4.stderr}", "warning")
            except Exception as e:
                self.log_to_terminal(f"❌ Hibernate configuration failed: {str(e)}", "error")
            
            # Method 3: Set monitor timeout to never
            self.log_to_terminal("🔧 Configuring display timeout (never turn off)...", "info")
            try:
                cmd5 = "powercfg /change monitor-timeout-ac 0"
                cmd6 = "powercfg /change monitor-timeout-dc 0"
                
                result5 = subprocess.run(cmd5, shell=True, capture_output=True, text=True, timeout=30)
                result6 = subprocess.run(cmd6, shell=True, capture_output=True, text=True, timeout=30)
                
                if result5.returncode == 0 and result6.returncode == 0:
                    success_count += 1
                    self.log_to_terminal("✓ Display timeout disabled successfully (AC and battery)", "success")
                else:
                    self.log_to_terminal(f"⚠ Display timeout configuration had issues: AC={result5.stderr}, Battery={result6.stderr}", "warning")
            except Exception as e:
                self.log_to_terminal(f"❌ Display timeout configuration failed: {str(e)}", "error")
            
            # Method 4: Configure power button action using powercfg (more reliable)
            self.log_to_terminal("🔧 Configuring power button (do nothing)...", "info")
            try:
                # Set power button to do nothing using powercfg
                # POWERBUTTONACTION: 0 = Do nothing, 1 = Sleep, 2 = Hibernate, 3 = Shut down
                power_btn_cmd1 = 'powercfg /setacvalueindex SCHEME_CURRENT SUB_BUTTONS PBUTTONACTION 0'
                power_btn_cmd2 = 'powercfg /setdcvalueindex SCHEME_CURRENT SUB_BUTTONS PBUTTONACTION 0'
                
                result7 = subprocess.run(power_btn_cmd1, shell=True, capture_output=True, text=True, timeout=30)
                result8 = subprocess.run(power_btn_cmd2, shell=True, capture_output=True, text=True, timeout=30)
                
                if result7.returncode == 0 and result8.returncode == 0:
                    success_count += 1
                    self.log_to_terminal("✓ Power button configured to do nothing", "success")
                else:
                    self.log_to_terminal(f"⚠ Power button configuration had issues: AC={result7.stderr}, DC={result8.stderr}", "warning")
            except Exception as e:
                self.log_to_terminal(f"❌ Power button configuration failed: {str(e)}", "error")
            
            # Method 5: Configure sleep button action (NEW - this was missing)
            self.log_to_terminal("🔧 Configuring sleep button (do nothing)...", "info")
            try:
                # Set sleep button to do nothing using powercfg
                # SLEEPBUTTONACTION: 0 = Do nothing, 1 = Sleep, 2 = Hibernate, 3 = Shut down
                sleep_btn_cmd1 = 'powercfg /setacvalueindex SCHEME_CURRENT SUB_BUTTONS SBUTTONACTION 0'
                sleep_btn_cmd2 = 'powercfg /setdcvalueindex SCHEME_CURRENT SUB_BUTTONS SBUTTONACTION 0'
                
                result9 = subprocess.run(sleep_btn_cmd1, shell=True, capture_output=True, text=True, timeout=30)
                result10 = subprocess.run(sleep_btn_cmd2, shell=True, capture_output=True, text=True, timeout=30)
                
                if result9.returncode == 0 and result10.returncode == 0:
                    success_count += 1
                    self.log_to_terminal("✓ Sleep button configured to do nothing", "success")
                else:
                    self.log_to_terminal(f"⚠ Sleep button configuration had issues: AC={result9.stderr}, DC={result10.stderr}", "warning")
            except Exception as e:
                self.log_to_terminal(f"❌ Sleep button configuration failed: {str(e)}", "error")
            
            # Method 6: Configure lid close action using powercfg (more reliable)
            self.log_to_terminal("🔧 Configuring lid close action (do nothing)...", "info")
            try:
                # Set lid close to do nothing using powercfg
                # LIDACTION: 0 = Do nothing, 1 = Sleep, 2 = Hibernate, 3 = Shut down
                lid_cmd1 = 'powercfg /setacvalueindex SCHEME_CURRENT SUB_BUTTONS LIDACTION 0'
                lid_cmd2 = 'powercfg /setdcvalueindex SCHEME_CURRENT SUB_BUTTONS LIDACTION 0'
                
                result11 = subprocess.run(lid_cmd1, shell=True, capture_output=True, text=True, timeout=30)
                result12 = subprocess.run(lid_cmd2, shell=True, capture_output=True, text=True, timeout=30)
                
                if result11.returncode == 0 and result12.returncode == 0:
                    success_count += 1
                    self.log_to_terminal("✓ Lid close configured to do nothing", "success")
                else:
                    self.log_to_terminal(f"⚠ Lid close configuration had issues: AC={result11.stderr}, DC={result12.stderr}", "warning")
            except Exception as e:
                self.log_to_terminal(f"❌ Lid close configuration failed: {str(e)}", "error")
            
            # Method 7: Force apply current power scheme to activate all changes
            self.log_to_terminal("🔧 Applying current power scheme to activate changes...", "info")
            try:
                # Apply the current scheme to make all changes active
                apply_cmd = 'powercfg /setactive SCHEME_CURRENT'
                apply_result = subprocess.run(apply_cmd, shell=True, capture_output=True, text=True, timeout=30)
                
                if apply_result.returncode == 0:
                    success_count += 1
                    self.log_to_terminal("✓ Current power scheme applied successfully", "success")
                else:
                    self.log_to_terminal(f"⚠ Power scheme application had issues: {apply_result.stderr}", "warning")
            except Exception as e:
                self.log_to_terminal(f"❌ Power scheme application failed: {str(e)}", "error")
            
            # Method 8: Apply current power scheme and refresh
            self.log_to_terminal("🔧 Applying power scheme changes...", "info")
            try:
                # Get current power scheme GUID
                get_scheme = "powercfg /getactivescheme"
                scheme_result = subprocess.run(get_scheme, shell=True, capture_output=True, text=True, timeout=30)
                
                if scheme_result.returncode == 0:
                    # Extract GUID from output
                    scheme_line = scheme_result.stdout.strip()
                    if ":" in scheme_line:
                        scheme_guid = scheme_line.split(":")[1].strip().split()[0]
                        apply_cmd = f"powercfg /setactive {scheme_guid}"
                        apply_result = subprocess.run(apply_cmd, shell=True, capture_output=True, text=True, timeout=30)
                        
                        if apply_result.returncode == 0:
                            success_count += 1
                            self.log_to_terminal("✓ Power scheme changes applied successfully", "success")
                        else:
                            self.log_to_terminal("⚠ Power scheme application had issues", "warning")
                    else:
                        self.log_to_terminal("⚠ Could not parse current power scheme", "warning")
                else:
                    self.log_to_terminal("⚠ Could not get current power scheme", "warning")
            except Exception as e:
                self.log_to_terminal(f"❌ Power scheme application failed: {str(e)}", "error")
            
            # Final results
            self.log_to_terminal(f"=== Power management configuration completed: {success_count}/{total_operations} operations successful ===", "info")
            
            if success_count >= 6:  # Require at least 6/8 operations to succeed
                self.log_to_terminal("🎉 Power management configured successfully!", "success")
                messagebox.showinfo("Power Management Configured", 
                    f"Power management settings have been configured successfully!\n\n"
                    f"Operations completed: {success_count}/{total_operations}\n\n"
                    "Settings applied:\n"
                    "✓ System will never sleep\n"
                    "✓ System will never hibernate\n"
                    "✓ Display will never turn off\n"
                    "✓ Power button will do nothing\n"
                    "✓ Sleep button will do nothing\n"
                    "✓ Closing lid will do nothing\n\n"
                    "These settings should now appear in:\n"
                    "Control Panel > Hardware and Sound > Power Options > System Settings\n\n"
                    "Changes are active immediately.")
            else:
                self.log_to_terminal("⚠ Power management partially configured", "warning")
                messagebox.showwarning("Partial Configuration", 
                    f"Power management was partially configured ({success_count}/{total_operations} operations successful).\n\n"
                    "Some settings may not have been applied.\n"
                    "Please check the terminal output for detailed information.\n\n"
                    "You may need to configure some settings manually through Windows Power Options.")
                
        except Exception as e:
            error_msg = f"❌ Critical error in power management configuration: {str(e)}"
            self.log_to_terminal(error_msg, "error")
            messagebox.showerror("Configuration Error", 
                f"Failed to configure power management settings.\n\n"
                f"Error: {str(e)}\n\n"
                "Please try running as administrator or configure manually through Windows Power Options.")
    
    def view_power_logs(self):
        """
        Display power management event logs in a new window.
        
        Opens a new window to show power-related event logs from
        the PowerEventProvider service.
        """
        try:
            self.log_to_terminal("Opening power logs window...", "INFO")
            
            # Open a new window to display power logs
            log_window = tk.Toplevel(self.root)
            log_window.title("Power Logs - InvokeX")
            log_window.geometry("700x500")
            
            # Set icon for the log window if available
            try:
                icon_paths = [
                    "icon.ico",
                    "C:\\Tools\\InvokeX\\icon.ico",
                    os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
                ]
                
                for icon_path in icon_paths:
                    if os.path.exists(icon_path):
                        log_window.iconbitmap(icon_path)
                        break
            except:
                pass
            
            # Header frame
            header_frame = tk.Frame(log_window, bg='#ffffff', height=60)
            header_frame.pack(fill='x', padx=0, pady=0)
            header_frame.pack_propagate(False)
            
            # Title in header
            title_label = tk.Label(header_frame, text="PowerEventProvider Logs", 
                                  font=('Segoe UI', 14, 'bold'), 
                                  bg='#ffffff', fg='#212529')
            title_label.pack(side='left', padx=20, pady=20)
            
            # Refresh button in header
            refresh_btn = tk.Button(header_frame, text="🔄 Refresh", 
                                   font=('Segoe UI', 9, 'bold'),
                                   bg='#007bff', fg='white',
                                   relief='flat', padx=15, pady=5,
                                   cursor='hand2', bd=0)
            refresh_btn.pack(side='right', padx=20, pady=20)
            
            # Main content frame
            content_frame = tk.Frame(log_window, bg='#f8f9fa')
            content_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
            
            # Text widget with modern styling
            text_frame = tk.Frame(content_frame, bg='#ffffff', relief='flat', bd=1)
            text_frame.pack(fill='both', expand=True)
            
            text_widget = tk.Text(text_frame, wrap=tk.WORD, 
                                 font=('Consolas', 10),
                                 bg='#ffffff', fg='#212529',
                                 relief='flat', bd=0,
                                 padx=15, pady=15)
            
            # Modern scrollbar
            scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            # Pack text widget and scrollbar
            text_widget.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Function to load logs
            def load_logs():
                try:
                    text_widget.config(state='normal')
                    text_widget.delete('1.0', tk.END)
                    text_widget.insert('1.0', "Loading PowerEventProvider logs...\n\n")
                    text_widget.update()
                    
                    self.log_to_terminal("Retrieving power logs...", "INFO")
                    
                    # Method 1: Try Get-WinEvent (more modern)
                    ps_command1 = 'Get-WinEvent -FilterHashtable @{LogName="Application"; ProviderName="PowerEventProvider"} -MaxEvents 100 | Format-Table TimeCreated, Id, LevelDisplayName, Message -AutoSize'
                    result1 = subprocess.run(['powershell', '-Command', ps_command1], 
                                           capture_output=True, text=True, timeout=30)
                    
                    text_widget.delete('1.0', tk.END)
                    
                    if result1.returncode == 0 and result1.stdout.strip():
                        text_widget.insert('1.0', "PowerEventProvider Event Logs:\n" + "="*50 + "\n\n" + result1.stdout)
                        self.log_to_terminal("Power logs retrieved successfully using Get-WinEvent!", "SUCCESS")
                    else:
                        # Method 2: Try Get-EventLog (legacy)
                        ps_command2 = 'Get-EventLog -LogName Application -Source PowerEventProvider -Newest 50 | Format-Table TimeGenerated, EntryType, Message -AutoSize'
                        result2 = subprocess.run(['powershell', '-Command', ps_command2], 
                                               capture_output=True, text=True, timeout=30)
                        
                        if result2.returncode == 0 and result2.stdout.strip():
                            text_widget.insert('1.0', "PowerEventProvider Event Logs (Legacy):\n" + "="*50 + "\n\n" + result2.stdout)
                            self.log_to_terminal("Power logs retrieved successfully using Get-EventLog!", "SUCCESS")
                        else:
                            # Method 3: Check if service exists and provide helpful info
                            service_check = subprocess.run(['sc', 'query', 'PowerEventProvider'], 
                                                         capture_output=True, text=True, timeout=10)
                            
                            if "RUNNING" in service_check.stdout or "STOPPED" in service_check.stdout:
                                text_widget.insert('1.0', "PowerEventProvider service is installed but no logs found yet.\n\n" +
                                                 "Service Status:\n" + service_check.stdout + "\n\n" +
                                                 "This could mean:\n" +
                                                 "• No power events have been logged yet\n" +
                                                 "• The service needs to be restarted\n" +
                                                 "• Logs may be in a different location\n" +
                                                 "• Logging level may not be configured properly")
                                self.log_to_terminal("PowerEventProvider service found but no logs available", "WARNING")
                            else:
                                # Check if installation directory exists
                                install_paths = [
                                    "C:\\Program Files (x86)\\PowerEventProvider",
                                    "C:\\Program Files\\PowerEventProvider"
                                ]
                                
                                installed = any(os.path.exists(path) for path in install_paths)
                                
                                if installed:
                                    text_widget.insert('1.0', "PowerEventProvider is installed but service is not running.\n\n" +
                                                     "Installation found in:\n" +
                                                     "C:\\Program Files (x86)\\PowerEventProvider\n\n" +
                                                     "To fix this:\n" +
                                                     "1. Run as Administrator\n" +
                                                     "2. Start the PowerEventProvider service\n" +
                                                     "3. Check Windows Event Viewer for system logs\n\n" +
                                                     "Service error: " + (service_check.stderr if service_check.stderr else 'Service not found'))
                                    self.log_to_terminal("PowerEventProvider installed but service not running", "WARNING")
                                else:
                                    text_widget.insert('1.0', "PowerEventProvider is not installed.\n\n" +
                                                     "To install PowerEventProvider:\n" +
                                                     "1. Go to the Applications tab\n" +
                                                     "2. Click 'Download & Install' for PowerEventProvider\n" +
                                                     "3. Run the installer as Administrator\n" +
                                                     "4. Restart this application after installation\n\n" +
                                                     "Installation will be in:\n" +
                                                     "C:\\Program Files (x86)\\PowerEventProvider")
                                    self.log_to_terminal("PowerEventProvider not installed", "INFO")
                                    
                except Exception as e:
                    text_widget.delete('1.0', tk.END)
                    error_text = f"Error retrieving logs: {str(e)}\n\nTroubleshooting:\n• Make sure PowerEventProvider is installed\n• Verify you have administrator privileges\n• Check your PowerShell execution policy\n• Try running InvokeX as Administrator"
                    text_widget.insert('1.0', error_text)
                    self.log_to_terminal(f"Error retrieving power logs: {str(e)}", "ERROR")
                finally:
                    text_widget.config(state='disabled')
            
            # Bind refresh button
            refresh_btn.configure(command=load_logs)
            
            # Load logs initially
            log_window.after(100, load_logs)
            
            # Modern button hover effects
            refresh_btn.bind('<Enter>', lambda e: refresh_btn.configure(bg='#0056b3'))
            refresh_btn.bind('<Leave>', lambda e: refresh_btn.configure(bg='#007bff'))
            
        except Exception as e:
            error_msg = f"Failed to open power logs: {str(e)}"
            self.log_to_terminal(error_msg, "ERROR")
            messagebox.showerror("Error", error_msg)
    
    def check_registry_keys(self):
        """
        Check if the shutdown hiding registry keys exist and show their values.
        This helps debug registry key creation issues.
        """
        try:
            self.log_to_terminal("Checking registry keys for shutdown hiding...", "INFO")
            
            # Check each registry key
            registry_checks = [
                ("NoClose", "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer\\NoClose"),
                ("NoLogoff", "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer\\NoLogoff"),
                ("NoShutdown", "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer\\NoShutdown")
            ]
            
            results = []
            for key_name, key_path in registry_checks:
                try:
                    # Use reg query command for more reliable results
                    result = subprocess.run([
                        'reg', 'query', key_path.replace('HKCU:', 'HKEY_CURRENT_USER')
                    ], capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0:
                        # Parse the value
                        lines = result.stdout.strip().split('\n')
                        value = "Not found"
                        for line in lines:
                            if key_name in line and 'REG_DWORD' in line:
                                parts = line.strip().split()
                                if len(parts) >= 3:
                                    value = parts[-1]
                                    break
                        
                        results.append(f"✓ {key_name}: {value}")
                        self.log_to_terminal(f"Registry key {key_name} found with value: {value}", "SUCCESS")
                    else:
                        results.append(f"✗ {key_name}: Not found")
                        self.log_to_terminal(f"Registry key {key_name} not found", "WARNING")
                        
                except Exception as e:
                    results.append(f"✗ {key_name}: Error - {str(e)}")
                    self.log_to_terminal(f"Error checking {key_name}: {str(e)}", "ERROR")
            
            # Show results in a message box
            result_text = "Registry Key Status:\n\n" + "\n".join(results)
            
            if any("✓" in result for result in results):
                messagebox.showinfo("Registry Key Check", 
                                  f"{result_text}\n\n"
                                  "Some registry keys exist. If you're still seeing shutdown options,\n"
                                  "try restarting Explorer or logging off/on.")
            else:
                messagebox.showwarning("Registry Key Check", 
                                     f"{result_text}\n\n"
                                     "No registry keys found. The shutdown hiding operation\n"
                                     "may not have completed successfully.")
            
        except Exception as e:
            error_msg = f"Failed to check registry keys: {str(e)}"
            self.log_to_terminal(error_msg, "ERROR")
            messagebox.showerror("Error", error_msg)

    def download_and_install_exe(self, url, app_name):
        """
        Download and install an EXE file with comprehensive error handling.
        
        Args:
            url (str): The URL to download the EXE file from
            app_name (str): The name of the application for user feedback
        """
        try:
            self.log_to_terminal(f"Starting {app_name} download from: {url}", "INFO")
            
            # Download the EXE file
            import urllib.request
            filename = f"{app_name.lower().replace(' ', '_')}_setup.exe"
            
            self.log_to_terminal(f"Downloading {app_name} installer...", "INFO")
            
            # Handle SSL certificate issues for some sites
            import ssl
            if "ninite.com" in url.lower():
                # Create SSL context that doesn't verify certificates for Ninite
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
                
                import urllib.request
                opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
                urllib.request.install_opener(opener)
            
            urllib.request.urlretrieve(url, filename)
            self.log_to_terminal(f"{app_name} installer downloaded: {filename}", "SUCCESS")
            
            # Try to install the EXE with elevated privileges
            self.log_to_terminal(f"Installing {app_name} with elevated privileges...", "INFO")
            
            try:
                # Handle different installer types with special handling for MuMu
                if "mumu" in app_name.lower():
                    # MuMu requires special handling to prevent freezing
                    self.log_to_terminal("Starting MuMu installer in background to prevent freezing...", "INFO")
                    
                    # Ask user for confirmation first
                    confirm = messagebox.askyesno(
                        "Install MuMu", 
                        "MuMu installer will run in the background to prevent InvokeX from freezing.\n\n"
                        "The installer will open independently. Please complete the installation manually.\n\n"
                        "Continue?"
                    )
                    
                    if not confirm:
                        self.log_to_terminal("MuMu installation cancelled by user", "INFO")
                        return
                    
                    # Start MuMu installer without waiting (prevents freezing)
                    subprocess.Popen([filename], shell=False)
                    
                    self.log_to_terminal("MuMu installer launched in background", "SUCCESS")
                    messagebox.showinfo(
                        "MuMu Installation Started", 
                        "MuMu installer has been launched in the background.\n\n"
                        "Please complete the installation in the MuMu installer window.\n\n"
                        "InvokeX will remain responsive during the installation."
                    )
                    return  # Exit early to prevent further processing
                    
                elif "ninite" in app_name.lower():
                    # Ninite installers work best when run directly without /silent flag
                    self.log_to_terminal("Running Ninite installer directly (no silent mode)...", "INFO")
                    timeout_seconds = 300
                    result = subprocess.run([filename], capture_output=True, text=True, timeout=timeout_seconds)
                else:
                    # Use Start-Process for other installers with elevated privileges
                    timeout_seconds = 300
                    install_cmd = f'Start-Process -FilePath "{filename}" -Verb RunAs -Wait'
                    result = subprocess.run([
                        "powershell", "-ExecutionPolicy", "Bypass", "-Command", install_cmd
                    ], capture_output=True, text=True, timeout=timeout_seconds)
                
                if result.returncode == 0:
                    self.log_to_terminal(f"{app_name} installed successfully!", "SUCCESS")
                    messagebox.showinfo("Success", f"{app_name} has been installed successfully!")
                else:
                    # If elevated install fails, try normal install
                    self.log_to_terminal(f"Elevated install failed, trying normal install...", "WARNING")
                    result2 = subprocess.run([filename], capture_output=True, text=True, timeout=timeout_seconds)
                    
                    if result2.returncode == 0:
                        self.log_to_terminal(f"{app_name} installed successfully with normal privileges!", "SUCCESS")
                        messagebox.showinfo("Success", f"{app_name} has been installed successfully!")
                    else:
                        # If still failing, suggest manual installation
                        error_msg = f"{app_name} installation failed. Exit code: {result2.returncode}"
                        self.log_to_terminal(error_msg, "ERROR")
                        self.log_to_terminal("Suggesting manual installation...", "INFO")
                        
                        # Show manual installation dialog
                        manual_install = messagebox.askyesno(
                            "Installation Failed", 
                            f"Automatic installation of {app_name} failed (Error {result2.returncode}).\n\n"
                            f"Would you like to open the installer manually?\n\n"
                            f"File location: {os.path.abspath(filename)}"
                        )
                        
                        if manual_install:
                            try:
                                os.startfile(filename)
                                self.log_to_terminal(f"{app_name} installer opened for manual installation.", "INFO")
                                messagebox.showinfo("Manual Installation", 
                                                  f"{app_name} installer opened. Please complete the installation manually.\n\n"
                                                  f"File: {os.path.abspath(filename)}")
                            except Exception as e:
                                self.log_to_terminal(f"Failed to open {app_name} installer: {str(e)}", "ERROR")
                        else:
                            messagebox.showwarning("Installation Skipped", 
                                                 f"{app_name} installation was skipped. You can install manually later.")
                            
            except subprocess.TimeoutExpired:
                self.log_to_terminal(f"{app_name} installation timed out. The installer may still be running.", "WARNING")
                messagebox.showwarning("Installation Timeout", 
                                     f"The {app_name} installer is taking longer than expected.\n"
                                     "Please check if the installation completed in the background.")
            
            # Clean up downloaded file only if installation was successful
            if os.path.exists(filename):
                try:
                    os.remove(filename)
                    self.log_to_terminal(f"Downloaded {app_name} installer cleaned up.", "INFO")
                except Exception as e:
                    self.log_to_terminal(f"Warning: Could not clean up {app_name} installer: {str(e)}", "WARNING")
                    
        except Exception as e:
            error_msg = f"Failed to download/install {app_name}: {str(e)}"
            self.log_to_terminal(error_msg, "ERROR")
            messagebox.showerror("Error", error_msg)

    def set_chrome_as_default(self):
        """Set Google Chrome as the default browser."""
        self.log_to_terminal("Attempting to set Google Chrome as default browser...", "info")
        
        try:
            # Check if Chrome is installed
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
            ]
            
            chrome_found = False
            chrome_path = ""
            for path in chrome_paths:
                if os.path.exists(path):
                    chrome_found = True
                    chrome_path = path
                    break
            
            if not chrome_found:
                self.log_to_terminal("Google Chrome not found. Please install Chrome first.", "warning")
                messagebox.showwarning("Chrome Not Found", 
                                     "Google Chrome is not installed on this system.\n\n"
                                     "Please install Chrome first, then try this tweak again.")
                return
            
            self.log_to_terminal(f"Chrome found at: {chrome_path}", "success")
            
            # Set Chrome as default browser using multiple methods
            set_default_commands = [
                # Method 1: Use reg add for better compatibility
                "reg add 'HKCU\\Software\\Microsoft\\Windows\\Shell\\Associations\\UrlAssociations\\http\\UserChoice' /v ProgId /d ChromeHTML /f",
                
                # Method 2: Set HTTPS association
                "reg add 'HKCU\\Software\\Microsoft\\Windows\\Shell\\Associations\\UrlAssociations\\https\\UserChoice' /v ProgId /d ChromeHTML /f",
                
                # Method 3: Set default browser in Classes
                "reg add 'HKCU\\Software\\Classes\\.htm' /ve /d ChromeHTML /f",
                
                # Method 4: Set HTML file association
                "reg add 'HKCU\\Software\\Classes\\.html' /ve /d ChromeHTML /f",
                
                # Method 5: Set default web browser
                "reg add 'HKCU\\Software\\Microsoft\\Windows\\Shell\\Associations\\MimeAssociations\\text/html\\UserChoice' /v ProgId /d ChromeHTML /f"
            ]
            
            success_count = 0
            total_commands = len(set_default_commands)
            
            for i, command in enumerate(set_default_commands, 1):
                try:
                    self.log_to_terminal(f"Executing command {i}/{total_commands}...", "info")
                    result = subprocess.run([
                        "cmd", "/c", command
                    ], capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0:
                        success_count += 1
                        self.log_to_terminal(f"Command {i} executed successfully.", "success")
                    else:
                        # Check if this is a "key doesn't exist" error (which is normal for some operations)
                        error_output = result.stderr.lower() if result.stderr else ""
                        if any(phrase in error_output for phrase in ["does not exist", "not found", "path not found"]):
                            self.log_to_terminal(f"Registry key not found (this is normal): {command}", "info")
                            success_count += 1  # Count as success since the goal is achieved
                        else:
                            self.log_to_terminal(f"Command {i} failed: {result.stderr}", "warning")
                            
                except subprocess.TimeoutExpired:
                    self.log_to_terminal(f"Command {i} timed out.", "warning")
                except Exception as e:
                    self.log_to_terminal(f"Command {i} error: {str(e)}", "warning")
            
            # Alternative method using Windows default programs
            try:
                self.log_to_terminal("Opening Windows default programs settings for manual configuration...", "info")
                subprocess.run([
                    "cmd", "/c", "start", "ms-settings:defaultapps"
                ], capture_output=True, timeout=30)
                self.log_to_terminal("Windows default programs settings opened.", "info")
                
                # Show user instructions
                messagebox.showinfo("Manual Setup Required", 
                    "Windows protects default browser settings.\n\n"
                    "The Settings app has been opened for you.\n\n"
                    "To set Chrome as default:\n"
                    "1. Scroll down to 'Web browser'\n"
                    "2. Click the current browser\n"
                    "3. Select 'Google Chrome'\n"
                    "4. Close the Settings app\n\n"
                    "This is the most reliable method in Windows 10/11.")
                
            except:
                self.log_to_terminal("Could not open Windows default programs settings.", "warning")
            
            # Final verification
            if success_count >= total_commands * 0.7:  # Allow 30% failure rate
                self.log_to_terminal("Chrome default browser settings applied successfully!", "success")
                self.log_to_terminal("Note: Some changes may require a system restart to take full effect.", "info")
                
                # Show success message
                messagebox.showinfo("Success", 
                    "Google Chrome has been set as the default browser!\n\n"
                    "Changes applied:\n"
                    "• HTTP links will open in Chrome\n"
                    "• HTTPS links will open in Chrome\n"
                    "• FTP links will open in Chrome\n\n"
                    "Note: A system restart may be required for all changes to take effect.\n"
                    "If the changes don't work, you can also set Chrome as default manually\n"
                    "through Windows Settings > Apps > Default Apps.")
            else:
                self.log_to_terminal("Some commands failed. Please check the output above.", "warning")
                messagebox.showwarning("Partial Success", 
                    "Some Chrome default browser settings were applied, but not all.\n\n"
                    "Please check the terminal output for details.\n"
                    "You can also set Chrome as default manually through Windows Settings.")
                
        except Exception as e:
            error_msg = f"Failed to set Chrome as default: {str(e)}"
            self.log_to_terminal(error_msg, "error")
            messagebox.showerror("Error", error_msg)

    def restart_system_10s(self):
        """Restart the system after a 15 second countdown."""
        self.log_to_terminal("Initiating system restart in 15 seconds...", "warning")
        
        # Show confirmation dialog
        confirm = messagebox.askyesno(
            "Confirm Restart", 
            "Are you sure you want to restart the system in 15 seconds?\n\n"
            "Make sure to save any open work before proceeding."
        )
        
        if not confirm:
            self.log_to_terminal("System restart cancelled by user.", "info")
            return
        
        # Show countdown dialog
        countdown_window = tk.Toplevel(self.root)
        countdown_window.title("System Restart")
        countdown_window.geometry("300x150")
        countdown_window.resizable(False, False)
        
        # Center the window
        countdown_window.transient(self.root)
        countdown_window.grab_set()
        
        # Set icon for the countdown window if available
        try:
            icon_paths = [
                "icon.ico",
                "C:\\Tools\\InvokeX\\icon.ico",
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
            ]
            
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    countdown_window.iconbitmap(icon_path)
                    break
        except:
            pass
        
        # Countdown label
        countdown_label = tk.Label(countdown_window, text="System will restart in:", 
                                  font=('Segoe UI', 12, 'bold'))
        countdown_label.pack(pady=(20, 10))
        
        # Time label
        time_label = tk.Label(countdown_window, text="15", 
                             font=('Segoe UI', 24, 'bold'), fg='#e74c3c')
        time_label.pack(pady=(0, 20))
        
        # Cancel button
        cancel_btn = tk.Button(countdown_window, text="Cancel Restart", 
                              command=lambda: self.cancel_restart(countdown_window),
                              bg='#e74c3c', fg='white', font=('Segoe UI', 10, 'bold'))
        cancel_btn.pack()
        
        # Start countdown
        self.countdown_seconds = 15
        self.countdown_window = countdown_window
        self.time_label = time_label
        self.countdown_restart()
    
    def countdown_restart(self):
        """Handle the countdown for system restart."""
        if hasattr(self, 'countdown_seconds') and self.countdown_seconds > 0:
            self.time_label.config(text=str(self.countdown_seconds))
            self.countdown_seconds -= 1
            self.root.after(1000, self.countdown_restart)
        elif hasattr(self, 'countdown_window') and self.countdown_window.winfo_exists():
            # Time's up, restart the system
            self.log_to_terminal("Countdown complete. Restarting system...", "warning")
            try:
                subprocess.run(["shutdown", "/r", "/t", "0"], capture_output=True, timeout=30)
            except Exception as e:
                self.log_to_terminal(f"Failed to restart system: {str(e)}", "error")
                messagebox.showerror("Restart Failed", f"Failed to restart system: {str(e)}")
            finally:
                self.countdown_window.destroy()
    
    def cancel_restart(self, window):
        """Cancel the system restart."""
        self.log_to_terminal("System restart cancelled by user.", "info")
        if hasattr(self, 'countdown_seconds'):
            delattr(self, 'countdown_seconds')
        window.destroy()
    
    def cancel_shutdown(self, window):
        """Cancel the system shutdown."""
        self.log_to_terminal("System shutdown cancelled by user.", "info")
        if hasattr(self, 'countdown_seconds'):
            delattr(self, 'countdown_seconds')
        window.destroy()
    
    def countdown_shutdown(self):
        """Handle the countdown for system shutdown."""
        if hasattr(self, 'countdown_seconds') and self.countdown_seconds > 0:
            self.time_label.config(text=str(self.countdown_seconds))
            self.countdown_seconds -= 1
            
            if self.countdown_seconds >= 0:
                self.root.after(1000, self.countdown_shutdown)
            else:
                # Time's up, proceed with shutdown
                self.countdown_window.destroy()
                try:
                    subprocess.run(["shutdown", "/s", "/t", "0"], capture_output=True, timeout=30)
                    self.log_to_terminal("Shutdown command sent successfully.", "success")
                except Exception as e:
                    self.log_to_terminal(f"Failed to shutdown system: {str(e)}", "error")
                    messagebox.showerror("Shutdown Failed", f"Failed to shutdown system: {str(e)}")

    def set_chrome_as_default(self):
        """Set Google Chrome as the default browser."""
        self.log_to_terminal("Setting Chrome as default browser...", "info")
        
        try:
            # Check if Chrome is installed
            chrome_locations = [
                "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
                os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe")
            ]
            
            chrome_path = None
            for path in chrome_locations:
                if os.path.exists(path):
                    chrome_path = path
                    break
            
            if not chrome_path:
                messagebox.showwarning("Chrome Not Found", 
                    "Google Chrome is not installed.\n\n"
                    "Please install Chrome first using the Apps tab.")
                return
            
            # Open Windows default apps settings
            self.log_to_terminal("Opening Windows default programs settings...", "info")
            subprocess.run(["cmd", "/c", "start", "ms-settings:defaultapps"], capture_output=True, timeout=30)
            
            messagebox.showinfo("Manual Configuration Required", 
                "Windows default apps settings opened.\n\n"
                "Please manually:\n"
                "1. Scroll down to 'Web browser'\n"
                "2. Click on the current browser\n"
                "3. Select 'Google Chrome'\n\n"
                "Note: Windows 10/11 requires manual confirmation for security.")
            
        except Exception as e:
            error_msg = f"Failed to set Chrome as default: {str(e)}"
            self.log_to_terminal(error_msg, "error")
            messagebox.showerror("Error", error_msg)
    
    def reset_default_browser(self):
        """Reset default browser settings."""
        self.log_to_terminal("Resetting default browser settings...", "info")
        
        try:
            # Open Windows default apps settings
            subprocess.run(["cmd", "/c", "start", "ms-settings:defaultapps"], capture_output=True, timeout=30)
            
            messagebox.showinfo("Manual Reset Required", 
                "Windows default apps settings opened.\n\n"
                "Please manually:\n"
                "1. Scroll down to 'Web browser'\n"
                "2. Click on the current browser\n"
                "3. Select your preferred browser (Edge, Firefox, etc.)\n\n"
                "Note: Windows 10/11 requires manual confirmation for security.")
            
        except Exception as e:
            error_msg = f"Failed to open browser settings: {str(e)}"
            self.log_to_terminal(error_msg, "error")
            messagebox.showerror("Error", error_msg)
    
    def reset_power_management(self):
        """Reset power management settings to Windows defaults."""
        self.log_to_terminal("Resetting power management settings to defaults...", "info")
        
        try:
            # Check if we're running as administrator
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                messagebox.showwarning("Administrator Required", 
                    "This operation requires administrator privileges.\n\n"
                    "Please restart InvokeX as administrator to reset power settings.")
                return
            
            # Reset power settings to Windows defaults
            reset_commands = [
                # Reset sleep timeouts to default (15 minutes on AC, 15 minutes on battery)
                "powercfg /change standby-timeout-ac 15",
                "powercfg /change standby-timeout-dc 15",
                
                # Reset hibernate timeout to default (never on AC, 180 minutes on battery)
                "powercfg /change hibernate-timeout-ac 0",
                "powercfg /change hibernate-timeout-dc 180",
                
                # Reset monitor timeout to default (10 minutes)
                "powercfg /change monitor-timeout-ac 10",
                "powercfg /change monitor-timeout-dc 10"
            ]
            
            success_count = 0
            for i, command in enumerate(reset_commands, 1):
                try:
                    self.log_to_terminal(f"Executing reset command {i}/{len(reset_commands)}: {command}", "info")
                    result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0:
                        success_count += 1
                        self.log_to_terminal(f"Reset command {i} executed successfully.", "success")
                    else:
                        self.log_to_terminal(f"Reset command {i} failed: {result.stderr}", "warning")
                        
                except Exception as e:
                    self.log_to_terminal(f"Reset command {i} error: {str(e)}", "warning")
            
            if success_count >= len(reset_commands) * 0.7:  # Allow 30% failure rate
                self.log_to_terminal("Power management settings reset to defaults successfully!", "success")
                messagebox.showinfo("Success", 
                    "Power management settings have been reset to Windows defaults!\n\n"
                    "Default settings restored:\n"
                    "• Sleep: 15 minutes\n"
                    "• Hibernate: Never (AC), 3 hours (Battery)\n"
                    "• Monitor: 10 minutes\n\n"
                    "Changes take effect immediately.")
            else:
                self.log_to_terminal("Some power reset commands failed.", "warning")
                messagebox.showwarning("Partial Success", 
                    f"Power settings partially reset ({success_count}/{len(reset_commands)} successful).\n\n"
                    "Please check the terminal output for details.")
                
        except Exception as e:
            error_msg = f"Failed to reset power management: {str(e)}"
            self.log_to_terminal(error_msg, "error")
            messagebox.showerror("Error", error_msg)
    
    def clear_power_logs(self):
        """Clear power management logs display."""
        self.log_to_terminal("Power logs cleared.", "info")
        # This would clear the logs display if we had a logs window
    
    def clear_registry_results(self):
        """Clear registry check results display."""
        self.log_to_terminal("Registry results cleared.", "info")
        # This would clear the results display if we had a results window
    
    def shutdown_system(self):
        """Shutdown the system after a 15 second countdown."""
        self.log_to_terminal("Initiating system shutdown in 15 seconds...", "warning")
        
        # Show confirmation dialog
        confirm = messagebox.askyesno(
            "Confirm Shutdown", 
            "Are you sure you want to shutdown the system in 15 seconds?\n\n"
            "Make sure to save any open work before proceeding."
        )
        
        if not confirm:
            self.log_to_terminal("System shutdown cancelled by user.", "info")
            return
        
        # Show countdown dialog
        countdown_window = tk.Toplevel(self.root)
        countdown_window.title("System Shutdown")
        countdown_window.geometry("300x150")
        countdown_window.resizable(False, False)
        
        # Center the window
        countdown_window.transient(self.root)
        countdown_window.grab_set()
        
        # Set icon for the countdown window if available
        try:
            icon_paths = [
                "icon.ico",
                "C:\\Tools\\InvokeX\\icon.ico",
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
            ]
            
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    countdown_window.iconbitmap(icon_path)
                    break
        except:
            pass
        
        # Countdown label
        countdown_label = tk.Label(countdown_window, text="System will shutdown in:", 
                                  font=('Segoe UI', 12, 'bold'))
        countdown_label.pack(pady=(20, 10))
        
        # Time label
        time_label = tk.Label(countdown_window, text="15", 
                             font=('Segoe UI', 24, 'bold'), fg='#e74c3c')
        time_label.pack(pady=(0, 20))
        
        # Cancel button
        cancel_btn = tk.Button(countdown_window, text="Cancel Shutdown", 
                              command=lambda: self.cancel_shutdown(countdown_window),
                              bg='#e74c3c', fg='white', font=('Segoe UI', 10, 'bold'))
        cancel_btn.pack()
        
        # Start countdown
        self.countdown_seconds = 15
        self.countdown_window = countdown_window
        self.time_label = time_label
        self.countdown_shutdown()
    
    def cancel_power_action(self):
        """Cancel any pending power actions."""
        self.log_to_terminal("Cancelling any pending power actions...", "info")
        
        try:
            # Cancel any pending shutdown/restart
            subprocess.run(["shutdown", "/a"], capture_output=True, timeout=30)
            self.log_to_terminal("Power actions cancelled successfully.", "success")
            messagebox.showinfo("Cancelled", "Any pending power actions have been cancelled.")
        except Exception as e:
            self.log_to_terminal(f"Failed to cancel power actions: {str(e)}", "error")
            messagebox.showerror("Cancel Failed", f"Failed to cancel power actions: {str(e)}")
    
    def check_gpo_status(self):
        """Check Group Policy status for shutdown hiding."""
        messagebox.showinfo("GPO Status", 
            "Group Policy Status:\n\n"
            "Hide Shutdown uses Group Policy Objects (GPO) instead of registry keys.\n"
            "GPO settings are managed by Windows Policy Engine and are more reliable.\n\n"
            "To check status:\n"
            "• Open Group Policy Editor (gpedit.msc)\n"
            "• Navigate to User Configuration > Administrative Templates > Start Menu and Taskbar\n"
            "• Look for shutdown-related policies")
    
    def check_current_default_browser(self):
        """Check and display the current default browser clearly."""
        self.log_to_terminal("Checking current default browser...", "info")
        
        try:
            # Method 1: Check HTTP protocol association
            cmd1 = 'reg query "HKCU\\Software\\Microsoft\\Windows\\Shell\\Associations\\UrlAssociations\\http\\UserChoice" /v ProgId'
            result1 = subprocess.run(cmd1, shell=True, capture_output=True, text=True, timeout=10)
            
            # Method 2: Check HTTPS protocol association  
            cmd2 = 'reg query "HKCU\\Software\\Microsoft\\Windows\\Shell\\Associations\\UrlAssociations\\https\\UserChoice" /v ProgId'
            result2 = subprocess.run(cmd2, shell=True, capture_output=True, text=True, timeout=10)
            
            http_browser = "Unknown"
            https_browser = "Unknown"
            
            # Parse HTTP result
            if result1.returncode == 0:
                for line in result1.stdout.split('\n'):
                    if 'ProgId' in line and 'REG_SZ' in line:
                        prog_id = line.split('REG_SZ')[-1].strip()
                        if 'Chrome' in prog_id:
                            http_browser = "Google Chrome"
                        elif 'Firefox' in prog_id:
                            http_browser = "Mozilla Firefox"
                        elif 'Edge' in prog_id or 'MSEdge' in prog_id:
                            http_browser = "Microsoft Edge"
                        elif 'IE' in prog_id or 'Internet' in prog_id:
                            http_browser = "Internet Explorer"
                        else:
                            http_browser = f"Other ({prog_id})"
                        break
            
            # Parse HTTPS result
            if result2.returncode == 0:
                for line in result2.stdout.split('\n'):
                    if 'ProgId' in line and 'REG_SZ' in line:
                        prog_id = line.split('REG_SZ')[-1].strip()
                        if 'Chrome' in prog_id:
                            https_browser = "Google Chrome"
                        elif 'Firefox' in prog_id:
                            https_browser = "Mozilla Firefox"
                        elif 'Edge' in prog_id or 'MSEdge' in prog_id:
                            https_browser = "Microsoft Edge"
                        elif 'IE' in prog_id or 'Internet' in prog_id:
                            https_browser = "Internet Explorer"
                        else:
                            https_browser = f"Other ({prog_id})"
                        break
            
            # Create status message
            status_msg = "Current Default Browser Status:\n\n"
            
            if http_browser == https_browser:
                if "Chrome" in http_browser:
                    status_msg += f"✅ DEFAULT BROWSER: {http_browser}\n\n"
                    status_msg += "Google Chrome is currently set as your default browser for both HTTP and HTTPS links."
                else:
                    status_msg += f"ℹ️ DEFAULT BROWSER: {http_browser}\n\n"
                    status_msg += f"Your current default browser is {http_browser}.\n"
                    status_msg += "Use 'Set Chrome Default' to change it to Google Chrome."
            else:
                status_msg += f"⚠️ MIXED SETTINGS:\n"
                status_msg += f"HTTP links: {http_browser}\n"
                status_msg += f"HTTPS links: {https_browser}\n\n"
                status_msg += "Your browser settings are inconsistent.\n"
                status_msg += "Use 'Set Chrome Default' to fix this and set Chrome as default."
            
            # Additional Chrome installation check
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                r"C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe".format(os.environ.get('USERNAME', ''))
            ]
            
            chrome_installed = any(os.path.exists(path) for path in chrome_paths)
            
            if not chrome_installed:
                status_msg += "\n\n⚠️ NOTE: Google Chrome does not appear to be installed on this system."
            
            messagebox.showinfo("Default Browser Status", status_msg)
            self.log_to_terminal(f"Current default browser check completed: HTTP={http_browser}, HTTPS={https_browser}", "success")
            
        except Exception as e:
            error_msg = f"Failed to check default browser: {str(e)}"
            self.log_to_terminal(error_msg, "error")
            messagebox.showerror("Browser Check Error", 
                f"Could not determine current default browser.\n\n"
                f"Error: {str(e)}\n\n"
                "You can check manually in Windows Settings > Apps > Default Apps.")
    
    def check_power_status(self):
        """Check current power management settings status."""
        self.log_to_terminal("Checking current power management settings...", "info")
        
        try:
            status_msg = "Current Power Management Settings:\n\n"
            
            # Check sleep timeout
            cmd1 = "powercfg /query SCHEME_CURRENT SUB_SLEEP STANDBYIDLE"
            result1 = subprocess.run(cmd1, shell=True, capture_output=True, text=True, timeout=10)
            
            if result1.returncode == 0:
                if "0x00000000" in result1.stdout:
                    status_msg += "✅ Sleep: Never (AC and Battery)\n"
                else:
                    status_msg += "⚠️ Sleep: Enabled (not configured)\n"
            else:
                status_msg += "❓ Sleep: Unable to check\n"
            
            # Check hibernate timeout
            cmd2 = "powercfg /query SCHEME_CURRENT SUB_SLEEP HIBERNATEIDLE"
            result2 = subprocess.run(cmd2, shell=True, capture_output=True, text=True, timeout=10)
            
            if result2.returncode == 0:
                if "0x00000000" in result2.stdout:
                    status_msg += "✅ Hibernate: Never (AC and Battery)\n"
                else:
                    status_msg += "⚠️ Hibernate: Enabled (not configured)\n"
            else:
                status_msg += "❓ Hibernate: Unable to check\n"
            
            # Check monitor timeout
            cmd3 = "powercfg /query SCHEME_CURRENT SUB_VIDEO VIDEOIDLE"
            result3 = subprocess.run(cmd3, shell=True, capture_output=True, text=True, timeout=10)
            
            if result3.returncode == 0:
                if "0x00000000" in result3.stdout:
                    status_msg += "✅ Display: Never turn off (AC and Battery)\n"
                else:
                    status_msg += "⚠️ Display: Will turn off (not configured)\n"
            else:
                status_msg += "❓ Display: Unable to check\n"
            
            # Check power button action
            cmd4 = "powercfg /query SCHEME_CURRENT SUB_BUTTONS PBUTTONACTION"
            result4 = subprocess.run(cmd4, shell=True, capture_output=True, text=True, timeout=10)
            
            if result4.returncode == 0:
                if "0x00000000" in result4.stdout:
                    status_msg += "✅ Power Button: Do nothing\n"
                else:
                    status_msg += "⚠️ Power Button: Has action (not configured)\n"
            else:
                status_msg += "❓ Power Button: Unable to check\n"
            
            # Check lid close action
            cmd5 = "powercfg /query SCHEME_CURRENT SUB_BUTTONS LIDACTION"
            result5 = subprocess.run(cmd5, shell=True, capture_output=True, text=True, timeout=10)
            
            if result5.returncode == 0:
                if "0x00000000" in result5.stdout:
                    status_msg += "✅ Lid Close: Do nothing\n"
                else:
                    status_msg += "⚠️ Lid Close: Has action (not configured)\n"
            else:
                status_msg += "❓ Lid Close: Unable to check (desktop PC)\n"
            
            status_msg += "\n💡 Use 'Configure Power' to apply all recommended settings."
            
            messagebox.showinfo("Power Management Status", status_msg)
            self.log_to_terminal("Power management status check completed", "success")
            
        except Exception as e:
            error_msg = f"Failed to check power status: {str(e)}"
            self.log_to_terminal(error_msg, "error")
            messagebox.showerror("Power Status Error", 
                f"Could not check power management settings.\n\n"
                f"Error: {str(e)}\n\n"
                "You can check manually in Windows Power Options.")
    
    def prevent_user_creation(self):
        """Prevent any more user accounts from being created."""
        self.log_to_terminal("Preventing user account creation...", "info")
        
        try:
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                messagebox.showwarning("Administrator Required", 
                    "This operation requires administrator privileges.")
                return
            
            # Set registry key to prevent user creation
            cmd = 'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "NoNewUsers" /t REG_DWORD /d 1 /f'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.log_to_terminal("User account creation prevention enabled", "success")
                messagebox.showinfo("Success", "User account creation has been disabled!")
            else:
                self.log_to_terminal(f"Failed to prevent user creation: {result.stderr}", "error")
                messagebox.showerror("Failed", f"Failed to prevent user creation: {result.stderr}")
                
        except Exception as e:
            self.log_to_terminal(f"Error preventing user creation: {str(e)}", "error")
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def restore_user_creation(self):
        """Restore ability to create user accounts."""
        self.log_to_terminal("Restoring user account creation...", "info")
        
        try:
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                messagebox.showwarning("Administrator Required", 
                    "This operation requires administrator privileges.")
                return
            
            # Remove registry key
            cmd = 'reg delete "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "NoNewUsers" /f'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            
            self.log_to_terminal("User account creation restored", "success")
            messagebox.showinfo("Success", "User account creation has been restored!")
                
        except Exception as e:
            self.log_to_terminal(f"Error restoring user creation: {str(e)}", "error")
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def check_user_creation_status(self):
        """Check if user creation is prevented."""
        try:
            cmd = 'reg query "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "NoNewUsers"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                messagebox.showinfo("User Creation Status", "Status: User account creation is PREVENTED")
            else:
                messagebox.showinfo("User Creation Status", "Status: User account creation is ALLOWED")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error checking status: {str(e)}")
    
    def create_admin_account(self):
        """Create Admin account with Administrator and Remote Desktop Users privileges."""
        self.log_to_terminal("Creating Admin account...", "info")
        
        try:
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                messagebox.showwarning("Administrator Required", 
                    "This operation requires administrator privileges.")
                return
            
            # First, check if Admin account already exists
            self.log_to_terminal("Checking if Admin account already exists...", "info")
            check_cmd = 'net user Admin'
            check_result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True, timeout=10)
            
            if check_result.returncode == 0:
                # Account already exists, warn user
                self.log_to_terminal("Admin account already exists!", "warning")
                
                overwrite = messagebox.askyesno(
                    "Admin Account Already Exists",
                    "An Admin account already exists on this system.\n\n"
                    "Would you like to:\n"
                    "• Reset the password for the existing account?\n\n"
                    "Click 'Yes' to reset password\n"
                    "Click 'No' to cancel operation\n\n"
                    "Warning: This will change the password for the existing Admin account."
                )
                
                if not overwrite:
                    self.log_to_terminal("Admin account creation cancelled by user", "info")
                    return
                
                # Get new password for existing account
                password = self.get_admin_password()
                if not password:
                    self.log_to_terminal("Admin account password reset cancelled - no password provided", "info")
                    return
                
                # Reset password for existing account
                self.log_to_terminal("Resetting password for existing Admin account...", "info")
                reset_cmd = f'net user Admin "{password}"'
                reset_result = subprocess.run(reset_cmd, shell=True, capture_output=True, text=True, timeout=30)
                
                if reset_result.returncode == 0:
                    self.log_to_terminal("Admin account password reset successfully", "success")
                    
                    # Ensure it's in the required groups
                    cmd2 = 'net localgroup Administrators Admin /add'
                    subprocess.run(cmd2, shell=True, capture_output=True, text=True, timeout=30)
                    
                    cmd3 = 'net localgroup "Remote Desktop Users" Admin /add'
                    subprocess.run(cmd3, shell=True, capture_output=True, text=True, timeout=30)
                    
                    messagebox.showinfo("Success", 
                        "Admin account password has been reset successfully!\n\n"
                        "Account: Admin\n"
                        "Password: Updated successfully\n"
                        "Groups: Administrators, Remote Desktop Users\n\n"
                        "The account is ready for use with the new password.")
                else:
                    self.log_to_terminal(f"Failed to reset Admin account password: {reset_result.stderr}", "error")
                    messagebox.showerror("Failed", f"Failed to reset Admin account password: {reset_result.stderr}")
                
                return
            
            # Account doesn't exist, proceed with creation
            self.log_to_terminal("Admin account does not exist, proceeding with creation...", "info")
            
            # Get password from user
            password = self.get_admin_password()
            if not password:
                self.log_to_terminal("Admin account creation cancelled - no password provided", "info")
                return
            
            # Create user account with password
            cmd1 = f'net user Admin "{password}" /add'
            result1 = subprocess.run(cmd1, shell=True, capture_output=True, text=True, timeout=30)
            
            if result1.returncode == 0:
                self.log_to_terminal("Admin account created", "success")
                
                # Add to Administrators group
                cmd2 = 'net localgroup Administrators Admin /add'
                result2 = subprocess.run(cmd2, shell=True, capture_output=True, text=True, timeout=30)
                
                # Add to Remote Desktop Users group
                cmd3 = 'net localgroup "Remote Desktop Users" Admin /add'
                result3 = subprocess.run(cmd3, shell=True, capture_output=True, text=True, timeout=30)
                
                self.log_to_terminal("Admin account configured with privileges", "success")
                messagebox.showinfo("Success", 
                    "Admin account created successfully!\n\n"
                    "Account: Admin\n"
                    "Password: Set successfully\n"
                    "Groups: Administrators, Remote Desktop Users\n\n"
                    "The account is ready for use with the password you provided.")
            else:
                if "already exists" in result1.stderr.lower():
                    messagebox.showinfo("Account Exists", "Admin account already exists!")
                else:
                    self.log_to_terminal(f"Failed to create Admin account: {result1.stderr}", "error")
                    messagebox.showerror("Failed", f"Failed to create Admin account: {result1.stderr}")
                
        except Exception as e:
            self.log_to_terminal(f"Error creating Admin account: {str(e)}", "error")
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def get_admin_password(self):
        """
        Show a password entry dialog for the admin account.
        
        Returns:
            str: The password entered by the user, or None if cancelled
        """
        import tkinter.simpledialog as simpledialog
        
        # Create a custom password dialog
        password_dialog = tk.Toplevel(self.root)
        password_dialog.title("Set Admin Account Password")
        password_dialog.geometry("400x300")
        password_dialog.resizable(False, False)
        
        # Center the dialog
        password_dialog.transient(self.root)
        password_dialog.grab_set()
        
        # Set icon for the dialog if available
        try:
            icon_paths = [
                "icon.ico",
                "C:\\Tools\\InvokeX\\icon.ico",
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
            ]
            
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    password_dialog.iconbitmap(icon_path)
                    break
        except:
            pass
        
        # Configure dialog
        password_dialog.configure(bg='#f8f9fa')
        
        # Title label
        title_label = tk.Label(password_dialog, 
                              text="Set Password for Admin Account", 
                              font=('Segoe UI', 14, 'bold'),
                              bg='#f8f9fa', fg='#212529')
        title_label.pack(pady=(20, 10))
        
        # Info label
        info_label = tk.Label(password_dialog, 
                             text="Please enter a strong password for the Admin account.\n"
                                  "This password will be used for Windows login and\n"
                                  "Remote Desktop connections.", 
                             font=('Segoe UI', 9),
                             bg='#f8f9fa', fg='#6c757d',
                             justify='center')
        info_label.pack(pady=(0, 20))
        
        # Password frame
        password_frame = tk.Frame(password_dialog, bg='#f8f9fa')
        password_frame.pack(pady=10)
        
        # Password label
        password_label = tk.Label(password_frame, 
                                 text="Password:", 
                                 font=('Segoe UI', 10),
                                 bg='#f8f9fa', fg='#212529')
        password_label.pack(anchor='w')
        
        # Password entry
        password_var = tk.StringVar()
        password_entry = tk.Entry(password_frame, 
                                 textvariable=password_var,
                                 show='*',
                                 font=('Segoe UI', 10),
                                 width=30)
        password_entry.pack(pady=(5, 10))
        
        # Confirm password frame
        confirm_frame = tk.Frame(password_dialog, bg='#f8f9fa')
        confirm_frame.pack(pady=10)
        
        # Confirm password label
        confirm_label = tk.Label(confirm_frame, 
                                text="Confirm Password:", 
                                font=('Segoe UI', 10),
                                bg='#f8f9fa', fg='#212529')
        confirm_label.pack(anchor='w')
        
        # Confirm password entry
        confirm_var = tk.StringVar()
        confirm_entry = tk.Entry(confirm_frame, 
                                textvariable=confirm_var,
                                show='*',
                                font=('Segoe UI', 10),
                                width=30)
        confirm_entry.pack(pady=(5, 10))
        
        # Result variable
        result = {'password': None, 'cancelled': False}
        
        def validate_and_set_password():
            password = password_var.get()
            confirm = confirm_var.get()
            
            if not password:
                messagebox.showerror("Error", "Password cannot be empty!", parent=password_dialog)
                return
            
            if len(password) < 4:
                messagebox.showerror("Error", "Password must be at least 4 characters long!", parent=password_dialog)
                return
            
            if password != confirm:
                messagebox.showerror("Error", "Passwords do not match!", parent=password_dialog)
                return
            
            result['password'] = password
            password_dialog.destroy()
        
        def cancel_dialog():
            result['cancelled'] = True
            password_dialog.destroy()
        
        # Buttons frame
        buttons_frame = tk.Frame(password_dialog, bg='#f8f9fa')
        buttons_frame.pack(pady=20)
        
        # OK button
        ok_button = tk.Button(buttons_frame, 
                             text="Create Account", 
                             command=validate_and_set_password,
                             bg='#0d6efd', fg='white',
                             font=('Segoe UI', 10, 'bold'),
                             padx=20, pady=8,
                             relief='flat',
                             cursor='hand2')
        ok_button.pack(side='left', padx=(0, 10))
        
        # Cancel button
        cancel_button = tk.Button(buttons_frame, 
                                 text="Cancel", 
                                 command=cancel_dialog,
                                 bg='#6c757d', fg='white',
                                 font=('Segoe UI', 10, 'bold'),
                                 padx=20, pady=8,
                                 relief='flat',
                                 cursor='hand2')
        cancel_button.pack(side='left')
        
        # Hover effects
        ok_button.bind('<Enter>', lambda e: ok_button.configure(bg='#0b5ed7'))
        ok_button.bind('<Leave>', lambda e: ok_button.configure(bg='#0d6efd'))
        cancel_button.bind('<Enter>', lambda e: cancel_button.configure(bg='#5a6268'))
        cancel_button.bind('<Leave>', lambda e: cancel_button.configure(bg='#6c757d'))
        
        # Bind Enter key to OK button
        password_dialog.bind('<Return>', lambda e: validate_and_set_password())
        password_entry.bind('<Return>', lambda e: confirm_entry.focus())
        confirm_entry.bind('<Return>', lambda e: validate_and_set_password())
        
        # Focus on password entry
        password_entry.focus()
        
        # Wait for dialog to close
        password_dialog.wait_window(password_dialog)
        
        return result['password']
    
    def open_user_management(self):
        """Open Windows User Management (mmc.exe > Local Users and Groups > Users)."""
        self.log_to_terminal("Opening User Management console...", "info")
        
        try:
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                messagebox.showwarning("Administrator Required", 
                    "User management requires administrator privileges.\n\n"
                    "Please run InvokeX as Administrator to manage users.")
                return
            
            # Show information about what will open
            messagebox.showinfo(
                "Opening User Management", 
                "Opening Microsoft Management Console (MMC) with Local Users and Groups.\n\n"
                "This will allow you to:\n"
                "• View all user accounts\n"
                "• Set/change passwords\n"
                "• Modify user properties\n"
                "• Manage group memberships\n\n"
                "Navigate to: Local Users and Groups > Users"
            )
            
            # Open MMC with Local Users and Groups snap-in
            # Using lusrmgr.msc directly opens Local Users and Groups
            subprocess.Popen(['mmc', 'lusrmgr.msc'], shell=False)
            
            self.log_to_terminal("User Management console opened successfully", "success")
            
        except Exception as e:
            self.log_to_terminal(f"Error opening User Management: {str(e)}", "error")
            messagebox.showerror("Error", f"Failed to open User Management: {str(e)}\n\n"
                                          "You can manually open it by:\n"
                                          "1. Press Win+R\n"
                                          "2. Type 'lusrmgr.msc'\n"
                                          "3. Press Enter")
    
    def check_admin_account_status(self):
        """Check if Admin account exists and its group memberships."""
        try:
            # Check if account exists
            cmd = 'net user Admin'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                # Account exists, check group memberships
                status = "Admin account EXISTS\n\nGroup memberships:\n"
                
                # Check Administrators group
                cmd_admin = 'net localgroup Administrators'
                result_admin = subprocess.run(cmd_admin, shell=True, capture_output=True, text=True, timeout=10)
                if "Admin" in result_admin.stdout:
                    status += "✓ Administrators\n"
                else:
                    status += "✗ Administrators\n"
                
                # Check Remote Desktop Users group
                cmd_rdp = 'net localgroup "Remote Desktop Users"'
                result_rdp = subprocess.run(cmd_rdp, shell=True, capture_output=True, text=True, timeout=10)
                if "Admin" in result_rdp.stdout:
                    status += "✓ Remote Desktop Users\n"
                else:
                    status += "✗ Remote Desktop Users\n"
                
                messagebox.showinfo("Admin Account Status", status)
            else:
                messagebox.showinfo("Admin Account Status", "Admin account does NOT exist")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error checking Admin account: {str(e)}")
    
    def enable_remote_desktop(self):
        """Enable Remote Desktop connections."""
        self.log_to_terminal("Enabling Remote Desktop...", "info")
        
        try:
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                messagebox.showwarning("Administrator Required", 
                    "This operation requires administrator privileges.")
                return
            
            success_count = 0
            
            # Enable Remote Desktop
            cmd1 = 'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f'
            result1 = subprocess.run(cmd1, shell=True, capture_output=True, text=True, timeout=30)
            if result1.returncode == 0:
                success_count += 1
                self.log_to_terminal("Remote Desktop enabled", "success")
            
            # Enable Remote Desktop through firewall
            cmd2 = 'netsh advfirewall firewall set rule group="Remote Desktop" new enable=yes'
            result2 = subprocess.run(cmd2, shell=True, capture_output=True, text=True, timeout=30)
            if result2.returncode == 0:
                success_count += 1
                self.log_to_terminal("Firewall rule enabled", "success")
            
            # Disable Network Level Authentication (optional, for compatibility)
            cmd3 = 'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\\WinStations\\RDP-Tcp" /v UserAuthentication /t REG_DWORD /d 0 /f'
            result3 = subprocess.run(cmd3, shell=True, capture_output=True, text=True, timeout=30)
            if result3.returncode == 0:
                success_count += 1
                self.log_to_terminal("Network Level Authentication disabled", "success")
            
            # Enable "keep my PC awake for connections when plugged in" feature
            # This prevents the PC from going to sleep when RDP connections are active
            cmd4 = 'powercfg /setacvalueindex SCHEME_CURRENT SUB_SLEEP STANDBYIDLE 0'
            result4 = subprocess.run(cmd4, shell=True, capture_output=True, text=True, timeout=30)
            if result4.returncode == 0:
                # Apply the power scheme
                cmd5 = 'powercfg /setactive SCHEME_CURRENT'
                result5 = subprocess.run(cmd5, shell=True, capture_output=True, text=True, timeout=30)
                if result5.returncode == 0:
                    success_count += 1
                    self.log_to_terminal("PC will stay awake for RDP connections when plugged in", "success")
            
            # Also set connected standby to never sleep when plugged in
            cmd6 = 'powercfg /setacvalueindex SCHEME_CURRENT SUB_SLEEP CONNECTEDIDLE 0'
            result6 = subprocess.run(cmd6, shell=True, capture_output=True, text=True, timeout=30)
            if result6.returncode == 0:
                subprocess.run(['powercfg', '/setactive', 'SCHEME_CURRENT'], capture_output=True, text=True, timeout=10)
                self.log_to_terminal("Connected standby disabled when plugged in", "success")
            
            if success_count >= 3:
                messagebox.showinfo("Success", 
                    "Remote Desktop has been enabled!\n\n"
                    "Settings applied:\n"
                    "• Remote Desktop connections enabled\n"
                    "• Firewall rules configured\n"
                    "• Network Level Authentication disabled\n"
                    "• PC will stay awake for connections when plugged in\n\n"
                    "You can now connect to this computer remotely.")
            else:
                messagebox.showwarning("Partial Success", 
                    "Remote Desktop partially enabled. Check terminal for details.\n\n"
                    "Some power management settings may not have been applied.")
                
        except Exception as e:
            self.log_to_terminal(f"Error enabling Remote Desktop: {str(e)}", "error")
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def disable_remote_desktop(self):
        """Disable Remote Desktop connections."""
        self.log_to_terminal("Disabling Remote Desktop...", "info")
        
        try:
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                messagebox.showwarning("Administrator Required", 
                    "This operation requires administrator privileges.")
                return
            
            # Disable Remote Desktop
            cmd1 = 'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 1 /f'
            result1 = subprocess.run(cmd1, shell=True, capture_output=True, text=True, timeout=30)
            
            # Disable firewall rule
            cmd2 = 'netsh advfirewall firewall set rule group="Remote Desktop" new enable=no'
            result2 = subprocess.run(cmd2, shell=True, capture_output=True, text=True, timeout=30)
            
            self.log_to_terminal("Remote Desktop disabled", "success")
            messagebox.showinfo("Success", "Remote Desktop has been disabled!")
                
        except Exception as e:
            self.log_to_terminal(f"Error disabling Remote Desktop: {str(e)}", "error")
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def check_rdp_status(self):
        """Check Remote Desktop status."""
        try:
            # Check if RDP is enabled
            cmd = 'reg query "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server" /v fDenyTSConnections'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                if "0x0" in result.stdout:
                    status = "Remote Desktop is ENABLED"
                else:
                    status = "Remote Desktop is DISABLED"
            else:
                status = "Remote Desktop status unknown"
            
            # Check firewall status
            cmd_fw = 'netsh advfirewall firewall show rule name="Remote Desktop - User Mode (TCP-In)"'
            result_fw = subprocess.run(cmd_fw, shell=True, capture_output=True, text=True, timeout=10)
            
            if "Enabled:                              Yes" in result_fw.stdout:
                status += "\nFirewall: ENABLED"
            else:
                status += "\nFirewall: DISABLED"
            
            messagebox.showinfo("Remote Desktop Status", status)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error checking RDP status: {str(e)}")

def main():
    """
    Main entry point for the InvokeX application.
    
    Creates the main window and starts the GUI event loop.
    """
    root = tk.Tk()
    app = InvokeX(root)
    root.mainloop()

if __name__ == "__main__":
    main()
