// ═══════════════════════════════════════════════════════════════
// InvokeX v2.0 — Preload Script (Context Bridge)
// ═══════════════════════════════════════════════════════════════
// This script runs in the preload context and exposes a safe
// `window.invokeX` API to the renderer via Electron's contextBridge.
// It is the ONLY bridge between renderer.js and main.js.
//
// Each method maps to an ipcMain.handle() in main.js.
// IPC listeners forward streaming events from main → renderer.
// ═══════════════════════════════════════════════════════════════

const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('invokeX', {

    // ── System & Elevation ──
    checkAdmin: () => ipcRenderer.invoke('check-admin'),
    restartAsAdmin: () => ipcRenderer.invoke('restart-as-admin'),
    getWindowsVersion: () => ipcRenderer.invoke('get-windows-version'),

    // ── PowerShell Execution ──
    runPowerShell: (command) => ipcRenderer.invoke('run-powershell', command),
    runPowerShellWindow: (command) => ipcRenderer.invoke('run-powershell-window', command),

    // ── Download & Install ──
    downloadAndInstallExe: (url, appName) => ipcRenderer.invoke('download-and-install-exe', url, appName),
    downloadAndInstallMsi: (url, appName) => ipcRenderer.invoke('download-and-install-msi', url, appName),
    downloadPortable: (url, appName) => ipcRenderer.invoke('download-portable', url, appName),

    // ── App Status Checks ──
    checkAppInstalled: (appName) => ipcRenderer.invoke('check-app-installed', appName),

    // ── Shell & Browser ──
    openUrl: (url) => ipcRenderer.invoke('open-url', url),

    // ── Dialogs ──
    showConfirm: (title, message) => ipcRenderer.invoke('show-confirm', title, message),
    showMessage: (title, message, type) => ipcRenderer.invoke('show-message', title, message, type),
    browseForFile: (title, filters) => ipcRenderer.invoke('browse-for-file', title, filters),

    // ── IPC Streaming Listeners (main → renderer) ──
    onCommandOutput: (callback) => ipcRenderer.on('command-output', (_, data) => callback(data)),
    onCommandComplete: (callback) => ipcRenderer.on('command-complete', (_, data) => callback(data)),
    onDownloadProgress: (callback) => ipcRenderer.on('download-progress', (_, data) => callback(data)),
});
