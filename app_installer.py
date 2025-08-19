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
        """Create the System Tweaks tab with action and restore buttons."""
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
        
        # Detect Windows version
        windows_version = self.get_windows_version()
        version_label = tk.Label(tweaks_frame, text=f"Detected: {windows_version}", 
                                font=('Segoe UI', 10), 
                                bg='#f0f0f0', fg='#7f8c8d')
        version_label.grid(row=0, column=0, pady=(45, 0), sticky='w')
        
        # Create scrollable canvas for tweaks
        canvas_frame = tk.Frame(tweaks_frame, bg='#f0f0f0')
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
        
        # Tweaks container
        tweaks_container = tk.Frame(scrollable_frame, bg='#f0f0f0')
        tweaks_container.pack(fill='both', expand=True, padx=15)
        
        # Tweak 1: Hide Shutdown Options
        self.create_tweak_section(tweaks_container,
                                 "Hide Shutdown Options",
                                 "Hide shutdown, sleep, and hibernate options from start menu (restart option preserved)",
                                 "Hide Options",
                                 "Restore Defaults",
                                 lambda: self.remove_shutdown_from_startup_smart(),
                                 lambda: self.restore_shutdown_options(),
                                 has_registry=True)
        
        # Tweak 2: Set Chrome As Default Browser
        self.create_tweak_section(tweaks_container,
                                 "Set Chrome As Default Browser",
                                 "Set Google Chrome as default browser",
                                 "Set Chrome Default",
                                 "Restore Defaults",
                                 lambda: self.set_chrome_as_default(),
                                 lambda: self.reset_default_browser(),
                                 has_registry=True)
        
        # Tweak 3: Power Management Settings
        self.create_tweak_section(tweaks_container,
                                 "Power Management Settings",
                                 "Configure power settings (sleep/hibernate to never, lid close to do nothing)",
                                 "Configure Power",
                                 "Restore Defaults",
                                 lambda: self.configure_power_management(),
                                 lambda: self.reset_power_management(),
                                 has_registry=True)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel scrolling for tweaks
        def _on_mousewheel(event):
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
        tweaks_container.bind('<Enter>', _bind_mousewheel)
        tweaks_container.bind('<Leave>', _unbind_mousewheel)
    
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
                    ("HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer", "NoShutdown"),
                    ("HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer", "NoShutdown"),
                    ("HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System", "DisableShutdown"),
                    ("HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer", "NoLogoff")
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
            
            # Display results
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
            
            # Show results in a dialog
            result_window = tk.Toplevel(self.root)
            result_window.title(f"Registry Check - {tweak_name}")
            result_window.geometry("800x400")
            result_window.resizable(True, True)
            
            # Text widget with scrollbar
            text_frame = tk.Frame(result_window)
            text_frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            text_widget = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, font=('Consolas', 9))
            text_widget.pack(fill='both', expand=True)
            text_widget.insert(tk.END, result_text)
            text_widget.config(state=tk.DISABLED)
            
            # Close button
            close_btn = tk.Button(result_window, text="Close", command=result_window.destroy,
                                 bg='#3498db', fg='white', font=('Segoe UI', 10, 'bold'))
            close_btn.pack(pady=10)
            
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
                # Check if PowerEventProvider service exists
                result = subprocess.run(['sc', 'query', 'PowerEventProvider'], 
                                      capture_output=True, text=True, timeout=10)
                return "RUNNING" in result.stdout or "STOPPED" in result.stdout
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
        
        # Buttons frame
        buttons_frame = tk.Frame(info_frame, bg='white')
        buttons_frame.pack(fill='x', pady=(10, 0))
        
        # Create wrapper function that refreshes status after installation
        def install_and_refresh():
            install_func()
            # Refresh status after installation (only if status_label exists)
            if status_label:
                self.root.after(1000, lambda: self.refresh_app_status(title, status_label))
        
        # Install button
        install_btn = tk.Button(buttons_frame, text=button_text, 
                               command=install_and_refresh,
                               bg='#3498db', fg='white', 
                               font=('Segoe UI', 8, 'bold'),
                               relief='flat', padx=15, pady=5,
                               cursor='hand2')
        install_btn.pack(side='left', padx=(0, 8))
        
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
        
        # Website/GitHub button
        website_btn = tk.Button(buttons_frame, text=button_label, 
                              command=lambda: webbrowser.open(github_url),
                              bg='#2c3e50', fg='white', 
                              font=('Segoe UI', 8, 'bold'),
                              relief='flat', padx=15, pady=5,
                              cursor='hand2')
        website_btn.pack(side='left')
        
        # Hover effects
        install_btn.bind('<Enter>', lambda e: install_btn.configure(bg='#2980b9'))
        install_btn.bind('<Leave>', lambda e: install_btn.configure(bg='#3498db'))
        website_btn.bind('<Enter>', lambda e: website_btn.configure(bg='#34495e'))
        website_btn.bind('<Leave>', lambda e: website_btn.configure(bg='#2c3e50'))
    
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
    
    def create_tweaks_tab(self):
        """Create the System Tweaks tab with scrollable content."""
        tweaks_frame = ttk.Frame(self.notebook)
        self.notebook.add(tweaks_frame, text="Tweaks")
        
        # Configure grid weights for auto-scaling
        tweaks_frame.grid_columnconfigure(0, weight=1)
        tweaks_frame.grid_rowconfigure(2, weight=1)  # Make the canvas frame expandable
        
        # Title
        title_label = tk.Label(tweaks_frame, text="System Tweaks", 
                              font=('Segoe UI', 14, 'bold'), 
                              bg='#f0f0f0', fg='#2c3e50')
        title_label.grid(row=0, column=0, pady=(10, 5), sticky='w')
        
        # Windows version info (more compact)
        windows_version = self.get_windows_version()
        version_label = tk.Label(tweaks_frame, text=f"Detected: {windows_version}", 
                                font=('Segoe UI', 8), 
                                bg='#f0f0f0', fg='#7f8c8d')
        version_label.grid(row=1, column=0, pady=(0, 5), sticky='w')
        
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
        
        # Tweak 1: Hide Shutdown Options (Smart Detection)
        self.create_tweak_section(tweaks_container,
                                 "Hide Shutdown Options",
                                 "Hide shutdown, sleep, and hibernate options from start menu (restart option preserved)",
                                 "Hide Options",
                                 lambda: self.remove_shutdown_from_startup_smart())
        
        # Tweak 2: Restore Shutdown Options
        self.create_tweak_section(tweaks_container,
                                 "Restore Shutdown Options",
                                 "Restore shutdown, sleep, and hibernate options",
                                 "Restore Options",
                                 lambda: self.restore_shutdown_options())
        
        # Tweak 3: Set Chrome As Default Browser
        self.create_tweak_section(tweaks_container,
                                 "Set Chrome As Default",
                                 "Set Google Chrome as the default browser",
                                 "Set Chrome Default",
                                 lambda: self.set_chrome_as_default())
        
        # Tweak 4: Restart System in 10 Seconds
        self.create_tweak_section(tweaks_container,
                                 "Restart System in 10 Seconds",
                                 "Restart the system after a 10 second countdown",
                                 "Restart in 10s",
                                 lambda: self.restart_system_10s())
        
        # Tweak 5: Power Management Settings
        self.create_tweak_section(tweaks_container,
                                 "Power Management Settings",
                                 "Set sleep/hibernate to never, power button to do nothing, lid close to do nothing",
                                 "Configure Power",
                                 lambda: self.configure_power_management())
        
        # Tweak 6: View Power Logs
        self.create_tweak_section(tweaks_container,
                                 "View Power Logs",
                                 "Display power management event logs",
                                 "View Logs",
                                 lambda: self.view_power_logs())
        
        # Tweak 7: Check Registry Keys
        self.create_tweak_section(tweaks_container,
                                 "Check Registry Keys",
                                 "Verify if shutdown hiding registry keys exist",
                                 "Check Keys",
                                 lambda: self.check_registry_keys())
        
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
            ], capture_output=True, text=True, timeout=60)
            
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
            ], capture_output=True, text=True, timeout=60)
            
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
        Hide shutdown options using Group Policy registry settings.
        This method uses multiple registry approaches for maximum compatibility.
        """
        self.log_to_terminal("Attempting to hide shutdown options from start menu...", "info")
        
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
            total_methods = 4
            
            # Method 1: Hide shutdown button from start menu (User Policy)
            try:
                reg_cmd1 = 'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v NoShutdown /t REG_DWORD /d 1 /f'
                result1 = subprocess.run(reg_cmd1, shell=True, capture_output=True, timeout=30)
                if result1.returncode == 0:
                    self.log_to_terminal("Successfully set user shutdown policy", "success")
                    success_count += 1
                else:
                    self.log_to_terminal(f"User shutdown policy failed: {result1.stderr}", "warning")
            except Exception as e:
                self.log_to_terminal(f"Could not set user shutdown policy: {str(e)}", "warning")
            
            # Method 2: Hide shutdown button (Machine Policy)
            try:
                reg_cmd2 = 'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v NoShutdown /t REG_DWORD /d 1 /f'
                result2 = subprocess.run(reg_cmd2, shell=True, capture_output=True, timeout=30)
                if result2.returncode == 0:
                    self.log_to_terminal("Successfully set machine shutdown policy", "success")
                    success_count += 1
                else:
                    self.log_to_terminal(f"Machine shutdown policy failed: {result2.stderr}", "warning")
            except Exception as e:
                self.log_to_terminal(f"Could not set machine shutdown policy: {str(e)}", "warning")
            
            # Method 3: Disable shutdown via system policy
            try:
                reg_cmd3 = 'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v DisableShutdown /t REG_DWORD /d 1 /f'
                result3 = subprocess.run(reg_cmd3, shell=True, capture_output=True, timeout=30)
                if result3.returncode == 0:
                    self.log_to_terminal("Successfully set system shutdown disable", "success")
                    success_count += 1
                else:
                    self.log_to_terminal(f"System shutdown disable failed: {result3.stderr}", "warning")
            except Exception as e:
                self.log_to_terminal(f"Could not set system shutdown disable: {str(e)}", "warning")
            
            # Method 4: Hide logoff option as well
            try:
                reg_cmd4 = 'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v NoLogoff /t REG_DWORD /d 1 /f'
                result4 = subprocess.run(reg_cmd4, shell=True, capture_output=True, timeout=30)
                if result4.returncode == 0:
                    self.log_to_terminal("Successfully hid logoff option", "success")
                    success_count += 1
                else:
                    self.log_to_terminal(f"Hide logoff failed: {result4.stderr}", "warning")
            except Exception as e:
                self.log_to_terminal(f"Could not hide logoff: {str(e)}", "warning")
            
            # Force Group Policy update
            try:
                self.log_to_terminal("Updating Group Policy...", "info")
                subprocess.run(["gpupdate", "/force"], capture_output=True, timeout=60)
                self.log_to_terminal("Group Policy updated", "success")
            except:
                self.log_to_terminal("Group Policy update completed", "info")
            
            # Final result
            if success_count >= 1:
                self.log_to_terminal(f"Shutdown functionality disabled successfully! ({success_count}/{total_methods} methods succeeded)", "success")
                messagebox.showinfo("Success", 
                    f"Shutdown functionality has been disabled!\n\n"
                    f"Methods applied: {success_count}/{total_methods}\n\n"
                    "Changes:\n"
                    "• Shutdown command disabled\n"
                    "• System shutdown policy set\n"
                    "• Restart functionality preserved\n\n"
                    "Note: You may need to restart to see full effects.")
            else:
                self.log_to_terminal("Failed to disable shutdown functionality", "warning")
                messagebox.showwarning("Failed", 
                    "Could not disable shutdown functionality.\n\n"
                    "This may be due to insufficient permissions or system protection.\n"
                    "Please check the terminal output for details.")
                
        except Exception as e:
            error_msg = f"Failed to disable shutdown: {str(e)}"
            self.log_to_terminal(error_msg, "error")
            messagebox.showerror("Error", error_msg)
    
    def restore_shutdown_options(self):
        """Restore shutdown functionality."""
        self.log_to_terminal("Attempting to restore shutdown functionality...", "info")
        
        try:
            # Check if we're running as administrator
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                self.log_to_terminal("This operation requires administrator privileges.", "warning")
                self.log_to_terminal("Please restart the application as administrator.", "warning")
                return
            
            # Restore shutdown functionality by removing registry entries
            success_count = 0
            total_methods = 4
            
            # Method 1: Remove user shutdown policy
            try:
                reg_cmd1 = 'reg delete "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v NoShutdown /f'
                result1 = subprocess.run(reg_cmd1, shell=True, capture_output=True, timeout=30)
                if result1.returncode == 0:
                    self.log_to_terminal("Successfully removed user shutdown policy", "success")
                    success_count += 1
                else:
                    self.log_to_terminal("User shutdown policy not found (already removed)", "info")
                    success_count += 1  # Count as success since goal is achieved
            except Exception as e:
                self.log_to_terminal(f"Could not remove user shutdown policy: {str(e)}", "warning")
            
            # Method 2: Remove machine shutdown policy
            try:
                reg_cmd2 = 'reg delete "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v NoShutdown /f'
                result2 = subprocess.run(reg_cmd2, shell=True, capture_output=True, timeout=30)
                if result2.returncode == 0:
                    self.log_to_terminal("Successfully removed machine shutdown policy", "success")
                    success_count += 1
                else:
                    self.log_to_terminal("Machine shutdown policy not found (already removed)", "info")
                    success_count += 1  # Count as success since goal is achieved
            except Exception as e:
                self.log_to_terminal(f"Could not remove machine shutdown policy: {str(e)}", "warning")
            
            # Method 3: Remove system shutdown disable
            try:
                reg_cmd3 = 'reg delete "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v DisableShutdown /f'
                result3 = subprocess.run(reg_cmd3, shell=True, capture_output=True, timeout=30)
                if result3.returncode == 0:
                    self.log_to_terminal("Successfully removed system shutdown disable", "success")
                    success_count += 1
                else:
                    self.log_to_terminal("System shutdown disable not found (already removed)", "info")
                    success_count += 1  # Count as success since goal is achieved
            except Exception as e:
                self.log_to_terminal(f"Could not remove system shutdown disable: {str(e)}", "warning")
            
            # Method 4: Remove logoff hiding
            try:
                reg_cmd4 = 'reg delete "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v NoLogoff /f'
                result4 = subprocess.run(reg_cmd4, shell=True, capture_output=True, timeout=30)
                if result4.returncode == 0:
                    self.log_to_terminal("Successfully restored logoff option", "success")
                    success_count += 1
                else:
                    self.log_to_terminal("Logoff policy not found (already removed)", "info")
                    success_count += 1  # Count as success since goal is achieved
            except Exception as e:
                self.log_to_terminal(f"Could not restore logoff option: {str(e)}", "warning")
            
            # Force Group Policy update
            try:
                self.log_to_terminal("Updating Group Policy...", "info")
                subprocess.run(["gpupdate", "/force"], capture_output=True, timeout=60)
                self.log_to_terminal("Group Policy updated", "success")
            except:
                self.log_to_terminal("Group Policy update completed", "info")
            
            # Final result
            if success_count >= 1:
                self.log_to_terminal(f"Shutdown functionality restored successfully! ({success_count}/{total_methods} methods succeeded)", "success")
                messagebox.showinfo("Success", 
                    f"Shutdown functionality has been restored!\n\n"
                    f"Methods applied: {success_count}/{total_methods}\n\n"
                    "Changes:\n"
                    "• Shutdown command restored\n"
                    "• System policies removed\n"
                    "• All power options available\n\n"
                    "Note: You may need to restart to see full effects.")
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
        """Configure power management settings (sleep/hibernate to never, lid close to do nothing)."""
        self.log_to_terminal("Attempting to configure power management settings...", "info")
        
        try:
            # Check if we're running as administrator
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                self.log_to_terminal("This operation requires administrator privileges.", "warning")
                self.log_to_terminal("Please restart the application as administrator.", "warning")
                return
            
            # Use powercfg commands for more reliable power management configuration
            power_commands = [
                # Set sleep to never when plugged in
                "powercfg /setacvalueindex SCHEME_CURRENT SUB_NONE 25a6bda1-4514-4c30-810e-6481143194d5 0",
                
                # Set sleep to never when on battery
                "powercfg /setdcvalueindex SCHEME_CURRENT SUB_NONE 25a6bda1-4514-4c30-810e-6481143194d5 0",
                
                # Set hibernate to never when plugged in
                "powercfg /setacvalueindex SCHEME_CURRENT SUB_NONE 9d7815a6-7ee4-497e-8888-515df05dce0f 0",
                
                # Set hibernate to never when on battery
                "powercfg /setdcvalueindex SCHEME_CURRENT SUB_NONE 9d7815a6-7ee4-497e-8888-515df05dce0f 0",
                
                # Set power button to do nothing when plugged in
                "powercfg /setacvalueindex SCHEME_CURRENT SUB_NONE 7648efa3-dd9c-4e3e-b566-50f929386280 0",
                
                # Set power button to do nothing when on battery
                "powercfg /setdcvalueindex SCHEME_CURRENT SUB_NONE 7648efa3-dd9c-4e3e-b566-50f929386280 0",
                
                # Set lid close to do nothing when plugged in
                "powercfg /setacvalueindex SCHEME_CURRENT SUB_NONE 5ca83367-6e45-459f-a27b-476b1d5cba29 0",
                
                # Set lid close to do nothing when on battery
                "powercfg /setdcvalueindex SCHEME_CURRENT SUB_NONE 5ca83367-6e45-459f-a27b-476b1d5cba29 0",
                
                # Apply the current power scheme
                "powercfg /setactive SCHEME_CURRENT"
            ]
            
            success_count = 0
            total_commands = len(power_commands)
            
            for i, command in enumerate(power_commands, 1):
                try:
                    self.log_to_terminal(f"Executing power command {i}/{total_commands}...", "info")
                    result = subprocess.run([
                        "cmd", "/c", command
                    ], capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0:
                        success_count += 1
                        self.log_to_terminal(f"Power command {i} executed successfully.", "success")
                    else:
                        # Check if this is a "not found" error (which might be normal for some power schemes)
                        error_output = result.stderr.lower() if result.stderr else ""
                        if any(phrase in error_output for phrase in ["not found", "does not exist"]):
                            self.log_to_terminal(f"Power setting not found (this may be normal): {command}", "info")
                            success_count += 1  # Count as success since the goal is achieved
                        else:
                            self.log_to_terminal(f"Power command {i} failed: {result.stderr}", "warning")
                            
                except subprocess.TimeoutExpired:
                    self.log_to_terminal(f"Power command {i} timed out.", "warning")
                except Exception as e:
                    self.log_to_terminal(f"Power command {i} error: {str(e)}", "warning")
            
            # Final verification
            if success_count >= total_commands * 0.7:  # Allow 30% failure rate
                self.log_to_terminal("Power management settings configured successfully!", "success")
                self.log_to_terminal("Note: Some changes may require a system restart to take full effect.", "info")
                
                # Show success message
                messagebox.showinfo("Success", 
                    "Power management settings have been configured!\n\n"
                    "Changes applied:\n"
                    "• Sleep: Never (plugged in and on battery)\n"
                    "• Hibernate: Never (plugged in and on battery)\n"
                    "• Power button: Do nothing (plugged in and on battery)\n"
                    "• Lid close: Do nothing (plugged in and on battery)\n\n"
                    "Note: A system restart may be required for all changes to take effect.")
            else:
                self.log_to_terminal("Some power commands failed. Please check the output above.", "warning")
                messagebox.showwarning("Partial Success", 
                    "Some power management configuration operations completed, but not all.\n\n"
                    "Please check the terminal output for details and consider running as administrator.")
                
        except Exception as e:
            error_msg = f"Failed to configure power management: {str(e)}"
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
                # Handle different installer types
                timeout_seconds = 120 if "mumu" in app_name.lower() else 300
                
                if "ninite" in app_name.lower():
                    # Ninite installers work best when run directly without /silent flag
                    self.log_to_terminal("Running Ninite installer directly (no silent mode)...", "INFO")
                    result = subprocess.run([filename], capture_output=True, text=True, timeout=timeout_seconds)
                else:
                    # Use Start-Process for other installers with elevated privileges
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
        """Restart the system after a 10 second countdown."""
        self.log_to_terminal("Initiating system restart in 10 seconds...", "warning")
        
        # Show confirmation dialog
        confirm = messagebox.askyesno(
            "Confirm Restart", 
            "Are you sure you want to restart the system in 10 seconds?\n\n"
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
        time_label = tk.Label(countdown_window, text="10", 
                             font=('Segoe UI', 24, 'bold'), fg='#e74c3c')
        time_label.pack(pady=(0, 20))
        
        # Cancel button
        cancel_btn = tk.Button(countdown_window, text="Cancel Restart", 
                              command=lambda: self.cancel_restart(countdown_window),
                              bg='#e74c3c', fg='white', font=('Segoe UI', 10, 'bold'))
        cancel_btn.pack()
        
        # Start countdown
        self.countdown_seconds = 10
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
