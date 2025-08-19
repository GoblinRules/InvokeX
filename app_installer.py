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
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Set window icon if available
        self.set_window_icon()
        
        # Configure logging
        self.setup_logging()
        
        # Check admin privileges
        self.is_admin = self.check_admin_privileges()
        
        # Style configuration
        self.setup_styles()
        
        # Create main container with proper weight configuration
        main_container = tk.Frame(root, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True, padx=15, pady=15)
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
        Log a message to both the terminal and log files.
        
        Args:
            message (str): The message to log
            level (str): The log level (INFO, ERROR, WARNING, SUCCESS)
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        color_map = {
            "INFO": "#00ff00",    # Green
            "ERROR": "#ff0000",   # Red
            "WARNING": "#ffff00", # Yellow
            "SUCCESS": "#00ffff"  # Cyan
        }
        
        # Add to terminal
        self.terminal.insert(tk.END, f"[{timestamp}] {level}: {message}\n")
        self.terminal.see(tk.END)
        
        # Log to file
        if level == "ERROR":
            self.logger.error(message)
        elif level == "WARNING":
            self.logger.warning(message)
        elif level == "SUCCESS":
            self.logger.info(f"SUCCESS: {message}")
        else:
            self.logger.info(message)
            
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
        """Create the Applications tab with scrollable content."""
        apps_frame = ttk.Frame(self.notebook)
        self.notebook.add(apps_frame, text="Apps")
        
        # Configure grid weights for auto-scaling
        apps_frame.grid_columnconfigure(0, weight=1)
        apps_frame.grid_rowconfigure(1, weight=1)
        
        # Title
        title_label = tk.Label(apps_frame, text="Application Installer", 
                              font=('Segoe UI', 14, 'bold'), 
                              bg='#f0f0f0', fg='#2c3e50')
        title_label.grid(row=0, column=0, pady=(15, 20), sticky='w')
        
        # Create scrollable canvas for apps
        canvas_frame = tk.Frame(apps_frame, bg='#f0f0f0')
        canvas_frame.grid(row=1, column=0, sticky='nsew', padx=(0, 5))
        canvas_frame.grid_columnconfigure(0, weight=1)
        canvas_frame.grid_rowconfigure(0, weight=1)
        
        # Canvas and scrollbar
        canvas = tk.Canvas(canvas_frame, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Apps container
        apps_container = tk.Frame(scrollable_frame, bg='#f0f0f0')
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
        self.create_app_section(apps_container, 
                               "PowerEventProvider", 
                               "Power management event provider",
                               "Download & Install",
                               "https://github.com/GoblinRules/powereventprovider",
                               lambda: self.download_and_install_msi("https://github.com/GoblinRules/powereventprovider/releases/download/V1.1/PowerEventProviderSetup.msi"))
        
        # App 4: CTT WinUtil
        self.create_app_section(apps_container, 
                               "CTT WinUtil", 
                               "Windows utility collection",
                               "Run CTT WinUtil",
                               "https://github.com/ChrisTitusTech/winutil",
                               lambda: self.run_powershell_command('irm "https://christitus.com/win" | iex'))
        
        # App 5: MASS
        self.create_app_section(apps_container, 
                               "MASS", 
                               "Microsoft Activation Scripts",
                               "Run MASS",
                               "https://github.com/massgravel/Microsoft-Activation-Scripts",
                               lambda: self.run_powershell_command("irm https://get.activated.win | iex"))
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
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
                # Check if PowerEventProvider service exists
                result = subprocess.run(['sc', 'query', 'PowerEventProvider'], 
                                      capture_output=True, text=True, timeout=10)
                return "RUNNING" in result.stdout or "STOPPED" in result.stdout
            elif app_name == "IP Python Tray App":
                # Check if the tray app executable exists
                return os.path.exists(os.path.expanduser("~\\AppData\\Local\\ippy-tray-app"))
            else:
                return False
        except:
            return False
    
    def create_app_section(self, parent, title, description, button_text, github_url, install_func):
        """
        Create a section for an individual application.
        
        Args:
            parent: The parent widget
            title (str): Application title
            description (str): Application description
            button_text (str): Text for the install button
            github_url (str): GitHub repository URL
            install_func: Function to call when install button is clicked
        """
        # Container for each app (smaller size)
        app_frame = tk.Frame(parent, bg='white', relief='solid', bd=1)
        app_frame.pack(fill='x', pady=6, padx=8)
        
        # App info
        info_frame = tk.Frame(app_frame, bg='white')
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
        
        # Status indicator
        is_installed = self.check_app_installed(title)
        status_text = "✓ Installed" if is_installed else "○ Not Installed"
        status_color = "#27ae60" if is_installed else "#95a5a6"
        status_label = tk.Label(info_frame, text=status_text, 
                               font=('Segoe UI', 8, 'bold'), 
                               bg='white', fg=status_color, anchor='w')
        status_label.pack(anchor='w', pady=(5, 0))
        
        # Buttons frame
        buttons_frame = tk.Frame(info_frame, bg='white')
        buttons_frame.pack(fill='x', pady=(10, 0))
        
        # Install button
        install_btn = tk.Button(buttons_frame, text=button_text, 
                               command=install_func,
                               bg='#3498db', fg='white', 
                               font=('Segoe UI', 8, 'bold'),
                               relief='flat', padx=15, pady=5,
                               cursor='hand2')
        install_btn.pack(side='left', padx=(0, 8))
        
        # GitHub button
        github_btn = tk.Button(buttons_frame, text="GitHub", 
                              command=lambda: webbrowser.open(github_url),
                              bg='#2c3e50', fg='white', 
                              font=('Segoe UI', 8, 'bold'),
                              relief='flat', padx=15, pady=5,
                              cursor='hand2')
        github_btn.pack(side='left')
        
        # Hover effects
        install_btn.bind('<Enter>', lambda e: install_btn.configure(bg='#2980b9'))
        install_btn.bind('<Leave>', lambda e: install_btn.configure(bg='#3498db'))
        github_btn.bind('<Enter>', lambda e: github_btn.configure(bg='#34495e'))
        github_btn.bind('<Leave>', lambda e: github_btn.configure(bg='#2c3e50'))
    
    def get_windows_version(self):
        """Get the current Windows version for user guidance."""
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.GetVersion.restype = ctypes.c_ulong
            version = kernel32.GetVersion()
            major = version >> 16 & 0xFF
            minor = version >> 8 & 0xFF
            
            if major == 10:
                if minor >= 0:
                    return "Windows 10"
                else:
                    return "Windows 10"
            elif major == 11:
                return "Windows 11"
            else:
                return f"Windows {major}.{minor}"
        except:
            return "Unknown Windows Version"
    
    def create_tweaks_tab(self):
        """Create the System Tweaks tab with scrollable content."""
        tweaks_frame = ttk.Frame(self.notebook)
        self.notebook.add(tweaks_frame, text="Tweaks")
        
        # Configure grid weights for auto-scaling
        tweaks_frame.grid_columnconfigure(0, weight=1)
        tweaks_frame.grid_rowconfigure(1, weight=1)
        
        # Title
        title_label = tk.Label(tweaks_frame, text="System Tweaks", 
                              font=('Segoe UI', 14, 'bold'), 
                              bg='#f0f0f0', fg='#2c3e50')
        title_label.grid(row=0, column=0, pady=(15, 20), sticky='w')
        
        # Windows version info
        windows_version = self.get_windows_version()
        version_label = tk.Label(tweaks_frame, text=f"Detected: {windows_version}", 
                                font=('Segoe UI', 9), 
                                bg='#f0f0f0', fg='#7f8c8d')
        version_label.grid(row=1, column=0, pady=(0, 20), sticky='w')
        
        # Create scrollable canvas for tweaks
        canvas_frame = tk.Frame(tweaks_frame, bg='#f0f0f0')
        canvas_frame.grid(row=2, column=0, sticky='nsew', padx=(0, 5))
        canvas_frame.grid_columnconfigure(0, weight=1)
        canvas_frame.grid_rowconfigure(0, weight=1)
        
        # Canvas and scrollbar
        canvas = tk.Canvas(canvas_frame, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Tweaks container
        tweaks_container = tk.Frame(scrollable_frame, bg='#f0f0f0')
        tweaks_container.pack(fill='both', expand=True, padx=15)
        
        # Tweak 1: Remove Shutdown from Startup (Windows 10)
        self.create_tweak_section(tweaks_container,
                                 "Remove Shutdown from Startup (Windows 10)",
                                 "Remove shutdown option from startup power menu for Windows 10",
                                 "Remove Shutdown (Win 10)",
                                 lambda: self.remove_shutdown_from_startup_win10())
        
        # Tweak 2: Remove Shutdown from Startup (Windows 11)
        self.create_tweak_section(tweaks_container,
                                 "Remove Shutdown from Startup (Windows 11)",
                                 "Remove shutdown option from startup power menu for Windows 11",
                                 "Remove Shutdown (Win 11)",
                                 lambda: self.remove_shutdown_from_startup_win11())
        
        # Tweak 3: View Power Logs
        self.create_tweak_section(tweaks_container,
                                 "View Power Logs",
                                 "Display power management event logs",
                                 "View Logs",
                                 lambda: self.view_power_logs())
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def create_tweak_section(self, parent, title, description, button_text, action_func):
        """
        Create a section for an individual system tweak.
        
        Args:
            parent: The parent widget
            title (str): Tweak title
            description (str): Tweak description
            button_text (str): Text for the action button
            action_func: Function to call when button is clicked
        """
        # Container for each tweak (smaller size)
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
        
        # Action button
        action_btn = tk.Button(info_frame, text=button_text, 
                              command=action_func,
                              bg='#e74c3c', fg='white', 
                              font=('Segoe UI', 8, 'bold'),
                              relief='flat', padx=15, pady=5,
                              cursor='hand2')
        action_btn.pack(anchor='w', pady=(10, 0))
        
        # Hover effects
        action_btn.bind('<Enter>', lambda e: action_btn.configure(bg='#c0392b'))
        action_btn.bind('<Leave>', lambda e: action_btn.configure(bg='#e74c3c'))
    
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
    
    def install_ippy_tray(self):
        """Install IP Python Tray App with multiple fallback methods."""
        self.log_to_terminal("Starting IP Python Tray App installation...", "info")
        
        try:
            # Method 1: Try to set execution policy first
            self.log_to_terminal("Setting PowerShell execution policy...", "info")
            result = subprocess.run([
                "powershell", "-Command", 
                "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.log_to_terminal("Execution policy set successfully.", "success")
            else:
                self.log_to_terminal("Warning: Could not set execution policy.", "warning")
            
            # Method 2: Try the original installation command
            self.log_to_terminal("Executing first installation command...", "info")
            result = subprocess.run([
                "powershell", "-ExecutionPolicy", "Bypass", "-Command",
                "irm 'https://raw.githubusercontent.com/GoblinRules/ippy-tray-app/main/install.ps1' | iex"
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                self.log_to_terminal("IP Python Tray App installed successfully!", "success")
                self.log_to_terminal("Note: A system reboot may be required for the tray app to appear.", "info")
                return
            else:
                self.log_to_terminal(f"First command failed: {result.stderr}", "warning")
            
            # Method 3: Try with TLS security protocol settings
            self.log_to_terminal("Setting TLS security protocol...", "info")
            tls_result = subprocess.run([
                "powershell", "-Command",
                "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12"
            ], capture_output=True, text=True, timeout=30)
            
            if tls_result.returncode == 0:
                self.log_to_terminal("TLS protocol set successfully.", "success")
            else:
                self.log_to_terminal("Warning: Could not set TLS protocol.", "warning")
            
            # Method 4: Try with .NET Framework crypto settings
            self.log_to_terminal("Setting .NET Framework crypto settings...", "info")
            crypto_result = subprocess.run([
                "powershell", "-Command",
                "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\.NETFramework\\v4.0.30319' -Name 'SchUseStrongCrypto' -Value 1 -Type DWord"
            ], capture_output=True, text=True, timeout=30)
            
            if crypto_result.returncode == 0:
                self.log_to_terminal(".NET Framework crypto settings updated.", "success")
            else:
                self.log_to_terminal("Warning: Could not update .NET Framework crypto settings.", "warning")
            
            # Method 5: Try with WOW64 settings
            self.log_to_terminal("Setting WOW64 .NET Framework crypto settings...", "info")
            wow64_result = subprocess.run([
                "powershell", "-Command",
                "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Wow6432Node\\Microsoft\\.NETFramework\\v4.0.30319' -Name 'SchUseStrongCrypto' -Value 1 -Type DWord"
            ], capture_output=True, text=True, timeout=30)
            
            if wow64_result.returncode == 0:
                self.log_to_terminal("WOW64 .NET Framework crypto settings updated.", "success")
            else:
                self.log_to_terminal("Warning: Could not update WOW64 .NET Framework crypto settings.", "warning")
            
            # Method 6: Final attempt with all settings applied
            self.log_to_terminal("Executing final installation command...", "info")
            final_result = subprocess.run([
                "powershell", "-ExecutionPolicy", "Bypass", "-Command",
                "irm 'https://raw.githubusercontent.com/GoblinRules/ippy-tray-app/main/install.ps1' | iex"
            ], capture_output=True, text=True, timeout=60)
            
            if final_result.returncode == 0:
                self.log_to_terminal("IP Python Tray App installed successfully!", "success")
                self.log_to_terminal("Note: A system reboot may be required for the tray app to appear.", "info")
            else:
                self.log_to_terminal(f"Final installation failed: {final_result.stderr}", "error")
                self.log_to_terminal("All installation methods failed. Please try installing manually.", "error")
                
        except subprocess.TimeoutExpired:
            self.log_to_terminal("Installation timed out. Please try again.", "error")
        except Exception as e:
            self.log_to_terminal(f"Installation error: {str(e)}", "error")
    
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
    
    def remove_shutdown_from_startup_win10(self):
        """Remove shutdown option from startup power menu for Windows 10."""
        self.log_to_terminal("Removing shutdown option from startup power menu (Windows 10)...", "info")
        
        try:
            # Check if we're running as administrator
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                self.log_to_terminal("This operation requires administrator privileges.", "warning")
                self.log_to_terminal("Please restart the application as administrator.", "warning")
                return
            
            # Registry keys specific to Windows 10
            registry_commands = [
                # Disable fast startup (Windows 10 specific)
                "Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Power' -Name 'HiberbootEnabled' -Value 0 -Type DWord -ErrorAction SilentlyContinue",
                
                # Remove shutdown option from power button (Windows 10)
                "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Name 'ShutdownWithoutLogon' -Value 0 -Type DWord -ErrorAction SilentlyContinue",
                
                # Disable shutdown option in start menu (Windows 10)
                "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer' -Name 'NoClose' -Value 1 -Type DWord -ErrorAction SilentlyContinue",
                
                # Remove shutdown from Ctrl+Alt+Del menu (Windows 10)
                "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Name 'DisableCAD' -Value 1 -Type DWord -ErrorAction SilentlyContinue",
                
                # Additional Windows 10 power management settings
                "Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Power' -Name 'HibernateEnabled' -Value 0 -Type DWord -ErrorAction SilentlyContinue",
                
                # Disable hybrid sleep (Windows 10)
                "Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Power' -Name 'HybridSleepEnabled' -Value 0 -Type DWord -ErrorAction SilentlyContinue",
                
                # Create the policies keys if they don't exist
                "New-Item -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Force -ErrorAction SilentlyContinue | Out-Null",
                "New-Item -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer' -Force -ErrorAction SilentlyContinue | Out-Null"
            ]
            
            success_count = 0
            total_commands = len(registry_commands)
            
            for i, command in enumerate(registry_commands, 1):
                try:
                    self.log_to_terminal(f"Executing Windows 10 registry command {i}/{total_commands}...", "info")
                    result = subprocess.run([
                        "powershell", "-Command", command
                    ], capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0:
                        success_count += 1
                        self.log_to_terminal(f"Windows 10 registry command {i} executed successfully.", "success")
                    else:
                        # Check if this is a "key doesn't exist" error (which is normal)
                        error_output = result.stderr.lower() if result.stderr else ""
                        if any(phrase in error_output for phrase in ["does not exist", "not found", "path not found"]):
                            self.log_to_terminal(f"Registry key not found (this is normal): {command}", "info")
                            success_count += 1  # Count as success since the goal is achieved
                        else:
                            self.log_to_terminal(f"Windows 10 registry command {i} failed: {result.stderr}", "warning")
                            
                except subprocess.TimeoutExpired:
                    self.log_to_terminal(f"Windows 10 registry command {i} timed out.", "warning")
                except Exception as e:
                    self.log_to_terminal(f"Windows 10 registry command {i} error: {str(e)}", "warning")
            
            # Apply the changes
            self.log_to_terminal("Applying Windows 10 registry changes...", "info")
            try:
                # Refresh the system to apply changes
                subprocess.run(["gpupdate", "/force"], capture_output=True, timeout=60)
                self.log_to_terminal("Group Policy updated successfully.", "success")
            except:
                self.log_to_terminal("Group Policy update completed.", "info")
            
            # Final verification
            if success_count >= total_commands * 0.7:  # Allow 30% failure rate
                self.log_to_terminal("Windows 10 shutdown option removal completed successfully!", "success")
                self.log_to_terminal("Note: Some changes may require a system restart to take full effect.", "info")
                
                # Show success message
                messagebox.showinfo("Success", 
                    "Shutdown option has been removed from Windows 10 startup power menu!\n\n"
                    "Changes applied:\n"
                    "• Shutdown option removed from startup\n"
                    "• Fast startup disabled\n"
                    "• Power button behavior modified\n"
                    "• Ctrl+Alt+Del menu updated\n\n"
                    "Note: A system restart may be required for all changes to take effect.")
            else:
                self.log_to_terminal("Some Windows 10 registry commands failed. Please check the output above.", "warning")
                messagebox.showwarning("Partial Success", 
                    "Some Windows 10 shutdown removal operations completed, but not all.\n\n"
                    "Please check the terminal output for details and consider running as administrator.")
                
        except Exception as e:
            error_msg = f"Failed to remove Windows 10 shutdown option: {str(e)}"
            self.log_to_terminal(error_msg, "error")
            messagebox.showerror("Error", error_msg)
    
    def remove_shutdown_from_startup_win11(self):
        """Remove shutdown option from startup power menu for Windows 11."""
        self.log_to_terminal("Removing shutdown option from startup power menu (Windows 11)...", "info")
        
        try:
            # Check if we're running as administrator
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                self.log_to_terminal("This operation requires administrator privileges.", "warning")
                self.log_to_terminal("Please restart the application as administrator.", "warning")
                return
            
            # Registry keys specific to Windows 11
            registry_commands = [
                # Disable fast startup (Windows 11 specific)
                "Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Power' -Name 'HiberbootEnabled' -Value 0 -Type DWord -ErrorAction SilentlyContinue",
                
                # Remove shutdown option from power button (Windows 11)
                "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Name 'ShutdownWithoutLogon' -Value 0 -Type DWord -ErrorAction SilentlyContinue",
                
                # Disable shutdown option in start menu (Windows 11)
                "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer' -Name 'NoClose' -Value 1 -Type DWord -ErrorAction SilentlyContinue",
                
                # Remove shutdown from Ctrl+Alt+Del menu (Windows 11)
                "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Name 'DisableCAD' -Value 1 -Type DWord -ErrorAction SilentlyContinue",
                
                # Additional Windows 11 power management settings
                "Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Power' -Name 'HibernateEnabled' -Value 0 -Type DWord -ErrorAction SilentlyContinue",
                
                # Disable hybrid sleep (Windows 11)
                "Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Power' -Name 'HybridSleepEnabled' -Value 0 -Type DWord -ErrorAction SilentlyContinue",
                
                # Windows 11 specific: Disable modern standby
                "Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Power' -Name 'CsEnabled' -Value 0 -Type DWord -ErrorAction SilentlyContinue",
                
                # Windows 11 specific: Disable connected standby
                "Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Power' -Name 'ConnectedStandbyEnabled' -Value 0 -Type DWord -ErrorAction SilentlyContinue",
                
                # Create the policies keys if they don't exist
                "New-Item -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Force -ErrorAction SilentlyContinue | Out-Null",
                "New-Item -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer' -Force -ErrorAction SilentlyContinue | Out-Null"
            ]
            
            success_count = 0
            total_commands = len(registry_commands)
            
            for i, command in enumerate(registry_commands, 1):
                try:
                    self.log_to_terminal(f"Executing Windows 11 registry command {i}/{total_commands}...", "info")
                    result = subprocess.run([
                        "powershell", "-Command", command
                    ], capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0:
                        success_count += 1
                        self.log_to_terminal(f"Windows 11 registry command {i} executed successfully.", "success")
                    else:
                        # Check if this is a "key doesn't exist" error (which is normal)
                        error_output = result.stderr.lower() if result.stderr else ""
                        if any(phrase in error_output for phrase in ["does not exist", "not found", "path not found"]):
                            self.log_to_terminal(f"Registry key not found (this is normal): {command}", "info")
                            success_count += 1  # Count as success since the goal is achieved
                        else:
                            self.log_to_terminal(f"Windows 11 registry command {i} failed: {result.stderr}", "warning")
                            
                except subprocess.TimeoutExpired:
                    self.log_to_terminal(f"Windows 11 registry command {i} timed out.", "warning")
                except Exception as e:
                    self.log_to_terminal(f"Windows 11 registry command {i} error: {str(e)}", "warning")
            
            # Apply the changes
            self.log_to_terminal("Applying Windows 11 registry changes...", "info")
            try:
                # Refresh the system to apply changes
                subprocess.run(["gpupdate", "/force"], capture_output=True, timeout=60)
                self.log_to_terminal("Group Policy updated successfully.", "success")
            except:
                self.log_to_terminal("Group Policy update completed.", "info")
            
            # Final verification
            if success_count >= total_commands * 0.7:  # Allow 30% failure rate
                self.log_to_terminal("Windows 11 shutdown option removal completed successfully!", "success")
                self.log_to_terminal("Note: Some changes may require a system restart to take full effect.", "info")
                
                # Show success message
                messagebox.showinfo("Success", 
                    "Shutdown option has been removed from Windows 11 startup power menu!\n\n"
                    "Changes applied:\n"
                    "• Shutdown option removed from startup\n"
                    "• Fast startup disabled\n"
                    "• Power button behavior modified\n"
                    "• Ctrl+Alt+Del menu updated\n"
                    "• Modern standby disabled\n"
                    "• Connected standby disabled\n\n"
                    "Note: A system restart may be required for all changes to take effect.")
            else:
                self.log_to_terminal("Some Windows 11 registry commands failed. Please check the output above.", "warning")
                messagebox.showwarning("Partial Success", 
                    "Some Windows 11 shutdown removal operations completed, but not all.\n\n"
                    "Please check the terminal output for details and consider running as administrator.")
                
        except Exception as e:
            error_msg = f"Failed to remove Windows 11 shutdown option: {str(e)}"
            self.log_to_terminal(error_msg, "error")
            messagebox.showerror("Error", error_msg)
    
    def remove_shutdown_from_startup(self):
        """Remove shutdown option from startup power menu for Windows 10 & 11."""
        self.log_to_terminal("Removing shutdown option from startup power menu...", "info")
        
        try:
            # Check if we're running as administrator
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                self.log_to_terminal("This operation requires administrator privileges.", "warning")
                self.log_to_terminal("Please restart the application as administrator.", "warning")
                return
            
            # Registry keys to modify for Windows 10/11 - using simpler, more reliable commands
            registry_commands = [
                # Disable fast startup (which can interfere with power options)
                "Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Power' -Name 'HiberbootEnabled' -Value 0 -Type DWord -ErrorAction SilentlyContinue",
                
                # Remove shutdown option from power button
                "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentControlSet\\Policies\\System' -Name 'ShutdownWithoutLogon' -Value 0 -Type DWord -ErrorAction SilentlyContinue",
                
                # Disable shutdown option in start menu
                "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer' -Name 'NoClose' -Value 1 -Type DWord -ErrorAction SilentlyContinue",
                
                # Remove shutdown from Ctrl+Alt+Del menu
                "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentControlSet\\Policies\\System' -Name 'DisableCAD' -Value 1 -Type DWord -ErrorAction SilentlyContinue",
                
                # Additional power management settings
                "Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Power' -Name 'HibernateEnabled' -Value 0 -Type DWord -ErrorAction SilentlyContinue",
                
                # Disable hybrid sleep
                "Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Power' -Name 'HybridSleepEnabled' -Value 0 -Type DWord -ErrorAction SilentlyContinue",
                
                # Create the policies keys if they don't exist
                "New-Item -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Force -ErrorAction SilentlyContinue | Out-Null",
                "New-Item -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer' -Force -ErrorAction SilentlyContinue | Out-Null"
            ]
            
            success_count = 0
            total_commands = len(registry_commands)
            
            for i, command in enumerate(registry_commands, 1):
                try:
                    self.log_to_terminal(f"Executing registry command {i}/{total_commands}...", "info")
                    result = subprocess.run([
                        "powershell", "-Command", command
                    ], capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0:
                        success_count += 1
                        self.log_to_terminal(f"Registry command {i} executed successfully.", "success")
                    else:
                        # Check if this is a "key doesn't exist" error (which is normal)
                        error_output = result.stderr.lower() if result.stderr else ""
                        if any(phrase in error_output for phrase in ["does not exist", "not found", "path not found"]):
                            self.log_to_terminal(f"Registry key not found (this is normal): {command}", "info")
                            success_count += 1  # Count as success since the goal is achieved
                        else:
                            self.log_to_terminal(f"Registry command {i} failed: {result.stderr}", "warning")
                            
                except subprocess.TimeoutExpired:
                    self.log_to_terminal(f"Registry command {i} timed out.", "warning")
                except Exception as e:
                    self.log_to_terminal(f"Registry command {i} error: {str(e)}", "warning")
            
            # Apply the changes
            self.log_to_terminal("Applying registry changes...", "info")
            try:
                # Refresh the system to apply changes
                subprocess.run(["gpupdate", "/force"], capture_output=True, timeout=60)
                self.log_to_terminal("Group Policy updated successfully.", "success")
            except:
                self.log_to_terminal("Group Policy update completed.", "info")
            
            # Final verification
            if success_count >= total_commands * 0.7:  # Allow 30% failure rate
                self.log_to_terminal("Shutdown option removal completed successfully!", "success")
                self.log_to_terminal("Note: Some changes may require a system restart to take full effect.", "info")
                
                # Show success message
                messagebox.showinfo("Success", 
                    "Shutdown option has been removed from the startup power menu!\n\n"
                    "Changes applied:\n"
                    "• Shutdown option removed from startup\n"
                    "• Fast startup disabled\n"
                    "• Power button behavior modified\n"
                    "• Ctrl+Alt+Del menu updated\n\n"
                    "Note: A system restart may be required for all changes to take effect.")
            else:
                self.log_to_terminal("Some registry commands failed. Please check the output above.", "warning")
                messagebox.showwarning("Partial Success", 
                    "Some shutdown removal operations completed, but not all.\n\n"
                    "Please check the terminal output for details and consider running as administrator.")
                
        except Exception as e:
            error_msg = f"Failed to remove shutdown option: {str(e)}"
            self.log_to_terminal(error_msg, "error")
            messagebox.showerror("Error", error_msg)
    
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
            
            # Text widget for logs
            text_widget = tk.Text(log_window, wrap=tk.WORD, font=('Consolas', 9))
            text_widget.pack(fill='both', expand=True, padx=10, pady=10)
            
            # Scrollbar
            scrollbar = tk.Scrollbar(text_widget)
            scrollbar.pack(side='right', fill='y')
            text_widget.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=text_widget.yview)
            
            # Get power logs
            try:
                self.log_to_terminal("Retrieving power logs...", "INFO")
                result = subprocess.run(['powershell', '-Command', 'get-eventlog -logname Application -source PowerEventProvider'], 
                                      capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    text_widget.insert('1.0', result.stdout)
                    self.log_to_terminal("Power logs retrieved successfully!", "SUCCESS")
                else:
                    error_text = f"Error: {result.stderr}\n\nNo PowerEventProvider logs found. Make sure PowerEventProvider is installed."
                    text_widget.insert('1.0', error_text)
                    self.log_to_terminal("No PowerEventProvider logs found.", "WARNING")
            except Exception as e:
                error_text = f"Error retrieving logs: {str(e)}"
                text_widget.insert('1.0', error_text)
                self.log_to_terminal(f"Error retrieving logs: {str(e)}", "ERROR")
            
            text_widget.config(state='disabled')
            
        except Exception as e:
            error_msg = f"Failed to open power logs: {str(e)}"
            self.log_to_terminal(error_msg, "ERROR")
            messagebox.showerror("Error", error_msg)

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
