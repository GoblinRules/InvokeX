// ═══════════════════════════════════════════════════════════════
// InvokeX v2.0 — Main Process (Electron)
// ═══════════════════════════════════════════════════════════════
// This is the Electron main process. It handles:
//   - Window creation and lifecycle
//   - IPC handlers for renderer communication
//   - PowerShell command execution (embedded + windowed)
//   - File download & install (EXE / MSI)
//   - Application install-status checks
//   - System info queries (admin, Windows version)
//   - Logging to timestamped files in ./logs
// ═══════════════════════════════════════════════════════════════

const { app, BrowserWindow, ipcMain, shell, dialog } = require('electron');
const { spawn, exec, execSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const https = require('https');
const http = require('http');

let mainWindow;

// ──────────────────────────────────────────────
// Section 1: Logging
// ──────────────────────────────────────────────

// Logs dir: use userData for packaged builds (asar is read-only), __dirname for dev
let logsDir;
if (app.isPackaged) {
    logsDir = path.join(app.getPath('userData'), 'logs');
} else {
    logsDir = path.join(__dirname, 'logs');
}
if (!fs.existsSync(logsDir)) {
    fs.mkdirSync(logsDir, { recursive: true });
}

const logFileName = `invokex_${new Date().toISOString().replace(/[:.]/g, '').slice(0, 15)}.log`;
const logStream = fs.createWriteStream(path.join(logsDir, logFileName), { flags: 'a' });

/**
 * Write a log entry to the current session log file.
 * @param {'INFO'|'ERROR'|'WARNING'} level - Severity level
 * @param {string} message - Log message
 */
function writeLog(level, message) {
    const timestamp = new Date().toISOString();
    logStream.write(`${timestamp} | ${level.padEnd(7)} | ${message}\n`);
}

// ──────────────────────────────────────────────
// Section 2: Window Creation
// ──────────────────────────────────────────────

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1280,
        height: 860,
        minWidth: 900,
        minHeight: 600,
        icon: path.join(__dirname, 'assets', 'icon.ico'),
        autoHideMenuBar: true,
        backgroundColor: '#0a0a0f',
        show: false,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            nodeIntegration: false,
        }
    });

    mainWindow.loadFile('index.html');

    // Show window once DOM is ready to avoid white flash
    mainWindow.once('ready-to-show', () => {
        mainWindow.show();
    });
}

// ──────────────────────────────────────────────
// Section 3: App Lifecycle
// ──────────────────────────────────────────────

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    logStream.end();
    app.quit();
});

// ──────────────────────────────────────────────
// Section 4: Admin & Elevation
// ──────────────────────────────────────────────

// Check if the current process has admin privileges
ipcMain.handle('check-admin', async () => {
    try {
        execSync('net session', { stdio: 'ignore' });
        return true;
    } catch {
        return false;
    }
});

// Restart the app elevated (as administrator)
ipcMain.handle('restart-as-admin', async () => {
    // For portable builds, process.execPath points to the temp-extracted electron.exe
    // which is missing ffmpeg.dll when launched standalone. Use PORTABLE_EXECUTABLE_FILE
    // (set by electron-builder) to get the actual portable EXE path instead.
    const exePath = process.env.PORTABLE_EXECUTABLE_FILE || process.execPath;
    const args = process.argv.slice(1);
    try {
        // Build the PowerShell command with proper escaping for paths with spaces
        const escapedExe = exePath.replace(/'/g, "''");
        let psCommand = `Start-Process -FilePath '${escapedExe}' -Verb RunAs`;
        if (args.length > 0) {
            const escapedArgs = args.join(' ').replace(/'/g, "''");
            psCommand += ` -ArgumentList '${escapedArgs}'`;
        }

        writeLog('INFO', `Restarting as admin: ${psCommand}`);

        exec(`powershell -NoProfile -ExecutionPolicy Bypass -Command "${psCommand.replace(/"/g, '\\"')}"`, (err) => {
            if (err) {
                writeLog('ERROR', `Failed to relaunch as admin: ${err.message}`);
            }
        });

        // Give the elevated process a moment to launch before quitting
        setTimeout(() => {
            app.quit();
        }, 1500);
    } catch (e) {
        writeLog('ERROR', `restart-as-admin error: ${e.message}`);
        return { error: e.message };
    }
});

// ──────────────────────────────────────────────
// Section 5: PowerShell Execution
// ──────────────────────────────────────────────

/**
 * Run a PowerShell command with streaming output back to the renderer.
 * Output is sent line-by-line via 'command-output' IPC events.
 * Resolves when the process exits.
 */
ipcMain.handle('run-powershell', async (event, command) => {
    return new Promise((resolve) => {
        writeLog('INFO', `Running PowerShell: ${command}`);

        const ps = spawn('powershell', ['-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', command], {
            stdio: ['ignore', 'pipe', 'pipe'],
            windowsHide: true
        });

        ps.stdout.on('data', (data) => {
            const text = data.toString();
            writeLog('INFO', text.trim());
            mainWindow.webContents.send('command-output', { text, level: 'INFO' });
        });

        ps.stderr.on('data', (data) => {
            const text = data.toString();
            writeLog('ERROR', text.trim());
            mainWindow.webContents.send('command-output', { text, level: 'ERROR' });
        });

        ps.on('close', (code) => {
            writeLog('INFO', `PowerShell exited with code ${code}`);
            mainWindow.webContents.send('command-complete', { code });
            resolve({ code });
        });

        ps.on('error', (err) => {
            writeLog('ERROR', `PowerShell error: ${err.message}`);
            mainWindow.webContents.send('command-output', { text: err.message, level: 'ERROR' });
            resolve({ code: -1, error: err.message });
        });
    });
});

/**
 * Run PowerShell in a separate visible window (for CTT WinUtil, MASS, etc.).
 * Opens an elevated PowerShell window and runs the command detached.
 */
ipcMain.handle('run-powershell-window', async (event, command) => {
    writeLog('INFO', `Running PowerShell in new window: ${command}`);
    try {
        spawn('powershell', [
            '-NoProfile', '-ExecutionPolicy', 'Bypass',
            '-Command', `Start-Process powershell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -Command "${command.replace(/"/g, '\\"')}"' -Verb RunAs`
        ], { detached: true, shell: true, stdio: 'ignore' });
        return { success: true };
    } catch (e) {
        return { error: e.message };
    }
});

// ──────────────────────────────────────────────
// Section 6: File Download & Install (EXE / MSI)
// ──────────────────────────────────────────────

/**
 * Generic download helper. Follows HTTP redirects, reports progress,
 * and writes the file to disk. Calls `onComplete(filePath)` when done.
 *
 * @param {string} url           - URL to download
 * @param {string} filePath      - Local path to save to
 * @param {string} appName       - Display name for progress messages
 * @param {Function} onComplete  - Called with (filePath) after download
 * @param {Function} onError     - Called with (errorMessage)
 */
function downloadFile(url, filePath, appName, onComplete, onError) {
    const file = fs.createWriteStream(filePath);

    const doDownload = (downloadUrl) => {
        const protocol = downloadUrl.startsWith('https') ? https : http;
        protocol.get(downloadUrl, { headers: { 'User-Agent': 'InvokeX/2.0' } }, (response) => {

            // Follow redirects (GitHub releases use 302 → CDN)
            if (response.statusCode >= 300 && response.statusCode < 400 && response.headers.location) {
                mainWindow.webContents.send('command-output', { text: 'Following redirect...', level: 'INFO' });
                doDownload(response.headers.location);
                return;
            }

            // Check for HTTP errors
            if (response.statusCode !== 200) {
                mainWindow.webContents.send('command-output', { text: `Download failed: HTTP ${response.statusCode}`, level: 'ERROR' });
                file.close();
                try { fs.unlinkSync(filePath); } catch { }
                onError(`HTTP ${response.statusCode}`);
                return;
            }

            // Track download progress
            const totalBytes = parseInt(response.headers['content-length'] || '0', 10);
            let downloadedBytes = 0;

            response.on('data', (chunk) => {
                downloadedBytes += chunk.length;
                if (totalBytes > 0) {
                    const pct = Math.round((downloadedBytes / totalBytes) * 100);
                    mainWindow.webContents.send('download-progress', { percent: pct, appName });
                }
            });

            // Pipe response into file
            response.pipe(file);

            // IMPORTANT: Listen for 'close' (not 'finish') to ensure the file
            // handle is fully released before we try to spawn it. This prevents
            // the EBUSY error on Windows.
            file.on('close', () => {
                mainWindow.webContents.send('command-output', { text: `Download complete.`, level: 'SUCCESS' });
                onComplete(filePath);
            });

        }).on('error', (err) => {
            file.close();
            try { fs.unlinkSync(filePath); } catch { }
            mainWindow.webContents.send('command-output', { text: `Download error: ${err.message}`, level: 'ERROR' });
            onError(err.message);
        });
    };

    doDownload(url);
}

/**
 * Download and run an EXE installer.
 * The EXE is saved to a temp directory, spawned detached, and cleaned up on exit.
 */
ipcMain.handle('download-and-install-exe', async (event, url, appName) => {
    return new Promise((resolve) => {
        writeLog('INFO', `Downloading EXE for ${appName} from ${url}`);
        mainWindow.webContents.send('command-output', { text: `Downloading ${appName}...`, level: 'INFO' });

        const tempDir = app.getPath('temp');
        const fileName = `${appName.replace(/\s+/g, '_')}_installer.exe`;
        const filePath = path.join(tempDir, fileName);

        downloadFile(url, filePath, appName,
            // onComplete — file is fully written and closed
            (savedPath) => {
                mainWindow.webContents.send('command-output', { text: `Installing ${appName}...`, level: 'INFO' });

                const installer = spawn(savedPath, [], { detached: true, stdio: 'ignore' });

                installer.on('error', (err) => {
                    mainWindow.webContents.send('command-output', { text: `Install error: ${err.message}`, level: 'ERROR' });
                    resolve({ code: -1 });
                });

                installer.on('close', (code) => {
                    mainWindow.webContents.send('command-output', {
                        text: `${appName} installer exited with code ${code}`,
                        level: code === 0 ? 'SUCCESS' : 'WARNING'
                    });
                    try { fs.unlinkSync(savedPath); } catch { }
                    resolve({ code });
                });

                installer.unref();
            },
            // onError
            (errMsg) => {
                resolve({ code: -1, error: errMsg });
            }
        );
    });
});

/**
 * Download and run an MSI installer via msiexec /i /quiet.
 */
ipcMain.handle('download-and-install-msi', async (event, url, appName) => {
    return new Promise((resolve) => {
        writeLog('INFO', `Downloading MSI for ${appName} from ${url}`);
        mainWindow.webContents.send('command-output', { text: `Downloading ${appName} MSI...`, level: 'INFO' });

        const tempDir = app.getPath('temp');
        const fileName = `${appName.replace(/\s+/g, '_')}_installer.msi`;
        const filePath = path.join(tempDir, fileName);

        downloadFile(url, filePath, appName,
            // onComplete
            (savedPath) => {
                mainWindow.webContents.send('command-output', { text: `Installing ${appName} via MSI...`, level: 'INFO' });

                const msiInstall = spawn('msiexec', ['/i', savedPath, '/quiet', '/norestart'], { stdio: 'ignore' });

                msiInstall.on('close', (code) => {
                    mainWindow.webContents.send('command-output', {
                        text: `${appName} MSI installer exited with code ${code}`,
                        level: code === 0 ? 'SUCCESS' : 'WARNING'
                    });
                    try { fs.unlinkSync(savedPath); } catch { }
                    resolve({ code });
                });

                msiInstall.on('error', (err) => {
                    mainWindow.webContents.send('command-output', { text: `MSI install error: ${err.message}`, level: 'ERROR' });
                    resolve({ code: -1 });
                });
            },
            // onError
            (errMsg) => {
                resolve({ code: -1, error: errMsg });
            }
        );
    });
});

/**
 * Download a portable EXE to the user's Desktop (save only, no install).
 * Used for apps like TRIP, ClearShot, SlickClick where the EXE is the app itself.
 */
ipcMain.handle('download-portable', async (event, url, appName) => {
    return new Promise((resolve) => {
        writeLog('INFO', `Downloading portable ${appName} from ${url}`);
        mainWindow.webContents.send('command-output', { text: `Downloading ${appName} (portable)...`, level: 'INFO' });

        const desktopDir = app.getPath('desktop');
        const fileName = url.split('/').pop() || `${appName.replace(/\s+/g, '_')}.exe`;
        const filePath = path.join(desktopDir, fileName);

        downloadFile(url, filePath, appName,
            // onComplete — file saved to Desktop
            () => {
                mainWindow.webContents.send('command-output', {
                    text: `${appName} saved to Desktop as ${fileName}`,
                    level: 'SUCCESS'
                });
                resolve({ code: 0, path: filePath });
            },
            // onError
            (errMsg) => {
                mainWindow.webContents.send('command-output', { text: `Download failed: ${errMsg}`, level: 'ERROR' });
                resolve({ code: -1, error: errMsg });
            }
        );
    });
});

// ──────────────────────────────────────────────
// Section 7: App Install-Status Checks
// ──────────────────────────────────────────────

/**
 * Check if an application is installed by inspecting common filesystem
 * paths, registry entries, or service status. Returns true/false.
 */
ipcMain.handle('check-app-installed', async (event, appName) => {
    try {
        const checks = {
            // ── GoblinRules Apps ──
            'TRIP': () => {
                const paths = [
                    path.join(process.env.LOCALAPPDATA || '', 'TRIP', 'TRIP.exe'),
                    path.join(process.env.USERPROFILE || '', 'Desktop', 'TRIP.exe'),
                    'C:\\Tools\\TRIP\\TRIP.exe'
                ];
                return paths.some(p => fs.existsSync(p));
            },
            'ClearShot': () => {
                const paths = [
                    path.join(process.env.LOCALAPPDATA || '', 'ClearShot', 'ClearShot.exe'),
                    path.join(process.env.USERPROFILE || '', 'Desktop', 'ClearShot.exe'),
                    'C:\\Program Files\\ClearShot\\ClearShot.exe'
                ];
                return paths.some(p => fs.existsSync(p));
            },
            'SlickClick': () => {
                const paths = [
                    path.join(process.env.LOCALAPPDATA || '', 'SlickClick', 'SlickClick.exe'),
                    path.join(process.env.USERPROFILE || '', 'Desktop', 'SlickClick.exe'),
                    'C:\\Program Files\\SlickClick\\SlickClick.exe'
                ];
                return paths.some(p => fs.existsSync(p));
            },
            'PyAutoClicker': () => {
                const paths = [
                    path.join(process.env.USERPROFILE || '', 'Desktop', 'PyAutoClicker.lnk'),
                    'C:\\Tools\\PyAutoClicker\\auto_clicker.py',
                    path.join(process.env.APPDATA || '', 'Microsoft\\Windows\\Start Menu\\Programs\\PyAutoClicker\\PyAutoClicker.lnk')
                ];
                return paths.some(p => fs.existsSync(p));
            },
            'IP Python Tray App': () => {
                const paths = [
                    'C:\\Tools\\TRIP\\trip.py',
                    'C:\\Tools\\ippy-tray-app\\trip.py',
                    path.join(process.env.USERPROFILE || '', 'Desktop', 'TRIP.lnk')
                ];
                return paths.some(p => fs.existsSync(p));
            },

            // ── Third-Party Apps ──
            'PowerEventProvider': () => {
                try {
                    const result = execSync('sc query PowerEventProvider', { stdio: 'pipe' }).toString();
                    return result.includes('RUNNING') || result.includes('STOPPED');
                } catch { return false; }
            },
            'CTT WinUtil': () => true, // Always available (runs from web)
            'MASS': () => {
                try {
                    const result = execSync('cscript //nologo C:\\Windows\\System32\\slmgr.vbs /xpr', { stdio: 'pipe', timeout: 10000 }).toString();
                    return result.toLowerCase().includes('permanently activated');
                } catch { return false; }
            },
            'Tailscale': () => {
                const paths = [
                    'C:\\Program Files\\Tailscale\\tailscale.exe',
                    'C:\\Program Files (x86)\\Tailscale\\tailscale.exe'
                ];
                return paths.some(p => fs.existsSync(p));
            },
            'MuMu': () => {
                const paths = [
                    'C:\\Program Files\\MuMu Player 12\\shell\\MuMuPlayer.exe',
                    'C:\\Program Files\\Netease\\MuMuPlayer-12.0\\shell\\MuMuPlayer.exe'
                ];
                return paths.some(p => fs.existsSync(p));
            },
            'Ninite': () => {
                const apps = [
                    'C:\\Program Files\\7-Zip\\7z.exe',
                    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
                    'C:\\Program Files\\Mozilla Firefox\\firefox.exe',
                    'C:\\Program Files\\Notepad++\\notepad++.exe'
                ];
                return apps.every(p => fs.existsSync(p));
            }
        };

        if (checks[appName]) {
            return checks[appName]();
        }
        return false;
    } catch {
        return false;
    }
});

// ──────────────────────────────────────────────
// Section 8: Utility IPC Handlers
// ──────────────────────────────────────────────

// Open URL in the user's default browser
ipcMain.handle('open-url', async (event, url) => {
    shell.openExternal(url);
});

// Get Windows edition and version string
ipcMain.handle('get-windows-version', async () => {
    try {
        const result = execSync('wmic os get Caption,Version /value', { stdio: 'pipe' }).toString();
        const caption = result.match(/Caption=(.+)/)?.[1]?.trim() || 'Windows';
        const version = result.match(/Version=(.+)/)?.[1]?.trim() || '';
        return `${caption} ${version}`;
    } catch {
        return 'Windows';
    }
});

// Show a password-entry dialog (handled in renderer for custom styling)
ipcMain.handle('show-password-dialog', async () => {
    return null;
});

// Show a native Yes/No confirmation dialog
ipcMain.handle('show-confirm', async (event, title, message) => {
    const result = dialog.showMessageBoxSync(mainWindow, {
        type: 'question',
        buttons: ['Yes', 'No'],
        title: title,
        message: message
    });
    return result === 0;
});

// Show a native informational message dialog
ipcMain.handle('show-message', async (event, title, message, type) => {
    dialog.showMessageBoxSync(mainWindow, {
        type: type || 'info',
        buttons: ['OK'],
        title: title,
        message: message
    });
});

// ── File Browser Dialog ──
ipcMain.handle('browse-for-file', async (event, title, filters) => {
    const result = await dialog.showOpenDialog(mainWindow, {
        title: title || 'Select a file',
        properties: ['openFile'],
        filters: filters || [
            { name: 'Executables', extensions: ['exe', 'bat', 'cmd', 'ps1', 'lnk'] },
            { name: 'All Files', extensions: ['*'] }
        ]
    });
    return result.canceled ? null : result.filePaths[0];
});
