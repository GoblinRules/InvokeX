// ═══════════════════════════════════════════════════════════════
// InvokeX v2.0 — Renderer (Full Feature Set)
// ═══════════════════════════════════════════════════════════════
// This is the main renderer script. It drives the entire UI:
//
//   Section 1:  Application Definitions   (APPS array)
//   Section 2:  Tweak Definitions          (TWEAKS array)
//   Section 3:  Toast Notifications
//   Section 4:  Terminal Logging
//   Section 5:  Terminal Expand / Collapse / Drag
//   Section 6:  Results Popup (structured output viewer)
//   Section 7:  Password Dialog
//   Section 8:  Confirm Dialog
//   Section 9:  Page Navigation
//   Section 10: Search / Filter
//   Section 11: App Card Rendering
//   Section 12: Tweak Card Rendering
//   Section 13: Batch Operations
//   Section 14: Action Handler (dispatches button clicks)
//   Section 15: Theme System
//   Section 16: Keyboard Shortcuts
//   Section 17: System Info Sidebar
//   Section 18: Network Diagnostics (NetTriage)
//   Section 19: Network Tools Page Handlers
//   Section 20: Initialization
// ═══════════════════════════════════════════════════════════════

// ──────────────────────────────────────────────
// Section 1: Application Definitions
// ──────────────────────────────────────────────

const APPS = [
    {
        id: 'trip', name: 'TRIP (Tray IP)',
        description: 'Lightweight system tray IP monitor with notifications & overlay',
        url: 'https://github.com/GoblinRules/TRIP',
        checkName: 'TRIP', tags: ['network', 'utility'],
        buttons: [
            { text: 'Download Portable', style: 'primary', action: 'portable', url: 'https://github.com/GoblinRules/TRIP/releases/download/v2.3.0/TRIP.exe' },
            { text: 'Download Installer', style: 'secondary', action: 'exe', url: 'https://github.com/GoblinRules/TRIP/releases/download/v2.3.0/TRIP_Setup.exe' }
        ]
    },
    {
        id: 'clearshot', name: 'ClearShot',
        description: 'Screenshot tool with region capture, annotation editor & hotkeys',
        url: 'https://github.com/GoblinRules/ClearShot',
        checkName: 'ClearShot', tags: ['utility'],
        buttons: [
            { text: 'Download Portable', style: 'primary', action: 'portable', url: 'https://github.com/GoblinRules/ClearShot/releases/download/v1.0.4/ClearShot.exe' },
            { text: 'Download Installer', style: 'secondary', action: 'exe', url: 'https://github.com/GoblinRules/ClearShot/releases/download/v1.0.4/ClearShot_Setup_1.0.4.exe' }
        ]
    },
    {
        id: 'slickclick', name: 'SlickClick',
        description: 'Lightweight auto-clicker — set pace, pick targets, tray support',
        url: 'https://github.com/GoblinRules/SlickClick',
        checkName: 'SlickClick', tags: ['utility'],
        buttons: [
            { text: 'Download Portable', style: 'primary', action: 'portable', url: 'https://github.com/GoblinRules/SlickClick/releases/download/V1.3.1/SlickClick.exe' },
            { text: 'Download Installer', style: 'secondary', action: 'exe', url: 'https://github.com/GoblinRules/SlickClick/releases/download/V1.3.1/SlickClick_Setup_v1.3.1.exe' }
        ]
    },
    {
        id: 'pyautoclicker', name: 'PyAutoClicker',
        description: 'Automated clicking utility for Windows',
        url: 'https://github.com/GoblinRules/PyAutoClicker',
        checkName: 'PyAutoClicker', tags: ['utility'],
        buttons: [
            { text: 'Install', style: 'primary', action: 'powershell', command: 'irm https://raw.githubusercontent.com/GoblinRules/PyAutoClicker/main/install.ps1 | iex' }
        ]
    },
    {
        id: 'ippy-tray', name: 'IP Python Tray App',
        description: 'System tray IP address display utility (legacy)',
        url: 'https://github.com/GoblinRules/ippy-tray-app',
        checkName: 'IP Python Tray App', tags: ['network', 'utility'],
        buttons: [
            { text: 'Install', style: 'primary', action: 'powershell', command: 'irm https://raw.githubusercontent.com/GoblinRules/ippy-tray-app/main/install.ps1 | iex' }
        ]
    },
    {
        id: 'powereventprovider', name: 'PowerEventProvider',
        description: 'Power management event provider service',
        url: 'https://github.com/GoblinRules/powereventprovider',
        checkName: 'PowerEventProvider', tags: ['power', 'system'],
        buttons: [
            { text: 'Download & Install', style: 'primary', action: 'msi', url: 'https://github.com/GoblinRules/powereventprovider/releases/download/V1.1/PowerEventProviderSetup.msi' },
            { text: 'View Power Logs', style: 'secondary', action: 'powershell', command: 'Get-EventLog -LogName Application -Source "PowerEventProvider" -Newest 50 | Format-Table TimeGenerated, EntryType, Message -AutoSize -Wrap' }
        ]
    },
    {
        id: 'ctt-winutil', name: 'CTT WinUtil',
        description: 'Windows utility collection by ChrisTitusTech',
        url: 'https://github.com/ChrisTitusTech/winutil',
        checkName: 'CTT WinUtil', alwaysAvailable: true, tags: ['system', 'utility'],
        buttons: [
            { text: 'Run WinUtil', style: 'primary', action: 'powershell-window', command: 'irm https://christitus.com/win | iex' }
        ]
    },
    {
        id: 'mass', name: 'MASS',
        description: 'Microsoft Activation Scripts',
        url: 'https://github.com/massgravel/Microsoft-Activation-Scripts',
        checkName: 'MASS', tags: ['system'],
        buttons: [
            { text: 'Run MASS', style: 'primary', action: 'powershell-window', command: 'irm https://get.activated.win | iex' }
        ]
    },
    {
        id: 'tailscale', name: 'Tailscale',
        description: 'VPN and secure networking mesh',
        url: 'https://tailscale.com/',
        checkName: 'Tailscale', tags: ['network', 'security'],
        buttons: [
            { text: 'Download & Install', style: 'primary', action: 'exe', url: 'https://pkgs.tailscale.com/stable/tailscale-setup-latest.exe' }
        ]
    },
    {
        id: 'mumu', name: 'MuMu Player',
        description: 'Android emulator for Windows',
        url: 'https://www.mumuplayer.com/',
        checkName: 'MuMu', tags: ['utility'],
        buttons: [
            { text: 'Download & Install', style: 'primary', action: 'exe', url: 'https://a11.gdl.netease.com/MuMu_5.0.2_gw-overseas12_all_1754534682.exe?n=MuMu_5.0.2_lMBe7ZC.exe' }
        ]
    },
    {
        id: 'ninite', name: 'Ninite Installer',
        description: 'Essential apps bundle (7-Zip, Chrome, Firefox, Notepad++)',
        url: 'https://ninite.com/',
        checkName: 'Ninite', tags: ['utility', 'browser'],
        buttons: [
            { text: 'Download & Install', style: 'primary', action: 'exe', url: 'https://ninite.com/7zip-chrome-firefox-notepadplusplus/ninite.exe' }
        ]
    }
];

// ──────────────────────────────────────────────
// Section 2: Tweak Definitions
// ──────────────────────────────────────────────
// Tweaks are system configuration cards shown on the System Tweaks page.
// Each has an id, name, description, tags (for filtering), and buttons
// that run PowerShell commands or custom handler functions.

const TWEAKS = [
    {
        id: 'hide-shutdown', name: 'Hide Shutdown Options', tags: ['power', 'security'],
        description: 'Hide shutdown, sleep, and hibernate options from start menu via Group Policy',
        buttons: [
            { text: 'Hide Options', style: 'primary', action: 'powershell', command: `$regPath='HKLM:\\SOFTWARE\\Microsoft\\PolicyManager\\default\\Start\\HideShutDown';if(!(Test-Path $regPath)){New-Item -Path $regPath -Force|Out-Null};Set-ItemProperty -Path $regPath -Name 'value' -Value 1 -Force;$regPath2='HKLM:\\SOFTWARE\\Microsoft\\PolicyManager\\default\\Start\\HideSleep';if(!(Test-Path $regPath2)){New-Item -Path $regPath2 -Force|Out-Null};Set-ItemProperty -Path $regPath2 -Name 'value' -Value 1 -Force;$regPath3='HKLM:\\SOFTWARE\\Microsoft\\PolicyManager\\default\\Start\\HideHibernate';if(!(Test-Path $regPath3)){New-Item -Path $regPath3 -Force|Out-Null};Set-ItemProperty -Path $regPath3 -Name 'value' -Value 1 -Force;$regPath4='HKLM:\\SOFTWARE\\Microsoft\\PolicyManager\\default\\Start\\HideRestart';if(!(Test-Path $regPath4)){New-Item -Path $regPath4 -Force|Out-Null};Set-ItemProperty -Path $regPath4 -Name 'value' -Value 1 -Force;Write-Host 'Shutdown options hidden. Sign out and back in for changes to take effect.'` },
            { text: 'Restore Defaults', style: 'secondary', action: 'powershell', command: `@('HideShutDown','HideSleep','HideHibernate','HideRestart')|ForEach-Object{$p="HKLM:\\SOFTWARE\\Microsoft\\PolicyManager\\default\\Start\\$_";if(Test-Path $p){Set-ItemProperty -Path $p -Name 'value' -Value 0 -Force}};Write-Host 'Shutdown options restored.'` },
            { text: 'Check Status', style: 'secondary', action: 'powershell', command: `@('HideShutDown','HideSleep','HideHibernate','HideRestart')|ForEach-Object{$p="HKLM:\\SOFTWARE\\Microsoft\\PolicyManager\\default\\Start\\$_";if(Test-Path $p){$v=(Get-ItemProperty -Path $p -Name 'value' -EA SilentlyContinue).value;Write-Host "$_ = $v $(if($v -eq 1){'(HIDDEN)'}else{'(VISIBLE)'})" }else{Write-Host "$_ = Not configured (VISIBLE)"}}` }
        ]
    },
    {
        id: 'chrome-default', name: 'Set Chrome as Default Browser', tags: ['browser'],
        description: 'Set Google Chrome as the default web browser',
        buttons: [
            { text: 'Set Chrome Default', style: 'primary', action: 'powershell', command: `$cp='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';if(-not (Test-Path $cp)){Write-Host 'Chrome not found at expected path. Install Chrome first.';return};Write-Host 'Setting Chrome as default browser...';$sid=[System.Security.Principal.WindowsIdentity]::GetCurrent().User.Value;$prots=@('http','https','.htm','.html');foreach($p in $prots){$regBase="HKCU:\\Software\\Microsoft\\Windows\\Shell\\Associations\\UrlAssociations\\$p\\UserChoice";if($p.StartsWith('.')){$regBase="HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\FileExts\\$p\\UserChoice"};try{if(Test-Path $regBase){Remove-Item $regBase -Force -EA SilentlyContinue} }catch{}};Start-Process $cp -ArgumentList '--make-default-browser';Start-Sleep -Seconds 2;Write-Host 'Chrome has been launched with --make-default-browser flag.';Write-Host 'If prompted, confirm Chrome as your default browser.';Write-Host 'Alternatively, Settings will open for manual confirmation:';Start-Process 'ms-settings:defaultapps'` },
            { text: 'Check Current', style: 'secondary', action: 'powershell', command: `try{$h=(Get-ItemProperty 'HKCU:\\Software\\Microsoft\\Windows\\Shell\\Associations\\UrlAssociations\\http\\UserChoice' -EA SilentlyContinue).ProgId;$hs=(Get-ItemProperty 'HKCU:\\Software\\Microsoft\\Windows\\Shell\\Associations\\UrlAssociations\\https\\UserChoice' -EA SilentlyContinue).ProgId;Write-Host "HTTP handler: $h";Write-Host "HTTPS handler: $hs";if($h -like '*Chrome*'){Write-Host 'Chrome IS the default browser.'}else{Write-Host 'Chrome is NOT the default browser.'}}catch{Write-Host "Error: $_"}` }
        ]
    },
    {
        id: 'power-management', name: 'Power Management Settings', tags: ['power'],
        description: 'Never sleep, never hibernate, display always on, power button does nothing',
        buttons: [
            { text: 'Configure Power', style: 'primary', action: 'powershell', command: `Write-Host 'Configuring power settings...';powercfg /change standby-timeout-ac 0;powercfg /change standby-timeout-dc 0;powercfg /change hibernate-timeout-ac 0;powercfg /change hibernate-timeout-dc 0;powercfg /change monitor-timeout-ac 0;powercfg /change monitor-timeout-dc 0;powercfg -setacvalueindex SCHEME_CURRENT SUB_BUTTONS PBUTTONACTION 0;powercfg -setdcvalueindex SCHEME_CURRENT SUB_BUTTONS PBUTTONACTION 0;powercfg -setacvalueindex SCHEME_CURRENT SUB_BUTTONS LIDACTION 0;powercfg -setdcvalueindex SCHEME_CURRENT SUB_BUTTONS LIDACTION 0;powercfg /setactive SCHEME_CURRENT;powercfg /hibernate off;Write-Host 'Power management configured.'` },
            { text: 'Restore Defaults', style: 'secondary', action: 'powershell', command: `powercfg /change standby-timeout-ac 30;powercfg /change standby-timeout-dc 15;powercfg /change hibernate-timeout-ac 180;powercfg /change hibernate-timeout-dc 60;powercfg /change monitor-timeout-ac 10;powercfg /change monitor-timeout-dc 5;powercfg -setacvalueindex SCHEME_CURRENT SUB_BUTTONS PBUTTONACTION 1;powercfg -setdcvalueindex SCHEME_CURRENT SUB_BUTTONS PBUTTONACTION 1;powercfg /setactive SCHEME_CURRENT;Write-Host 'Power management restored.'` },
            { text: 'Check Status', style: 'secondary', action: 'powershell', command: `$plan=powercfg /getactivescheme;Write-Host "Active plan: $plan";$h=(Get-ItemProperty 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Power' -Name HibernateEnabled -EA SilentlyContinue).HibernateEnabled;Write-Host "Hibernate: $(if($h -eq 0){'Disabled'}else{'Enabled'})"` }
        ]
    },
    {
        id: 'power-actions', name: 'Power Actions', tags: ['power'],
        description: 'Quick power actions for system control (15-second countdown)',
        buttons: [
            { text: '🔄 Restart', style: 'danger', action: 'custom', confirm: true, confirmTitle: 'Restart System', confirmDesc: 'Restart in 15 seconds?', handler: async () => { logToTerminal('System will restart in 15 seconds... Run "shutdown /a" to cancel.', 'WARNING'); await window.invokeX.runPowerShell('shutdown /r /t 15'); } },
            { text: '⏻ Shutdown', style: 'danger', action: 'custom', confirm: true, confirmTitle: 'Shutdown System', confirmDesc: 'Shutdown in 15 seconds?', handler: async () => { logToTerminal('System will shutdown in 15 seconds...', 'WARNING'); await window.invokeX.runPowerShell('shutdown /s /t 15'); } },
            { text: '🚫 Cancel', style: 'secondary', action: 'powershell', command: 'shutdown /a; Write-Host "Power action cancelled."' }
        ]
    },
    {
        id: 'prevent-user-creation', name: 'Prevent User Account Creation', tags: ['security'],
        description: 'Prevent new user accounts from being created via Group Policy',
        buttons: [
            { text: 'Enable Protection', style: 'primary', action: 'powershell', confirm: true, confirmTitle: 'Enable Protection', confirmDesc: 'This will prevent new user account creation.', command: `$rp='HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System';Set-ItemProperty -Path $rp -Name 'NoConnectedUser' -Value 3 -Type DWord -Force;Set-ItemProperty -Path $rp -Name 'BlockUserFromShowingAccountDetailsOnSignin' -Value 1 -Type DWord -Force;Write-Host 'User account creation prevention enabled.'` },
            { text: 'Restore Defaults', style: 'secondary', action: 'powershell', command: `$rp='HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System';Remove-ItemProperty -Path $rp -Name 'NoConnectedUser' -EA SilentlyContinue;Remove-ItemProperty -Path $rp -Name 'BlockUserFromShowingAccountDetailsOnSignin' -EA SilentlyContinue;Write-Host 'Restrictions removed.'` },
            { text: 'Check Status', style: 'secondary', action: 'powershell', command: `$rp='HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System';$n=(Get-ItemProperty -Path $rp -Name 'NoConnectedUser' -EA SilentlyContinue).NoConnectedUser;$b=(Get-ItemProperty -Path $rp -Name 'BlockUserFromShowingAccountDetailsOnSignin' -EA SilentlyContinue).BlockUserFromShowingAccountDetailsOnSignin;Write-Host "NoConnectedUser: $(if($n -eq 3){'ENABLED (Blocked)'}else{'Not set (Allowed)'})";Write-Host "BlockAccountDetails: $(if($b -eq 1){'ENABLED'}else{'Not set'})"` }
        ]
    },
    {
        id: 'create-admin', name: 'Create Admin Account', tags: ['security'],
        description: 'Create "Admin" account with Administrators & Remote Desktop Users membership',
        buttons: [
            {
                text: 'Create Account', style: 'primary', action: 'custom', handler: async () => {
                    const pw = await showPasswordDialog(); if (!pw) return;
                    logToTerminal('Creating Admin account...', 'INFO');
                    await window.invokeX.runPowerShell(`$p=ConvertTo-SecureString '${pw.replace(/'/g, "''")}' -AsPlainText -Force;try{New-LocalUser -Name 'Admin' -Password $p -FullName 'Administrator' -Description 'Created by InvokeX' -PasswordNeverExpires -EA Stop;Add-LocalGroupMember -Group 'Administrators' -Member 'Admin' -EA SilentlyContinue;Add-LocalGroupMember -Group 'Remote Desktop Users' -Member 'Admin' -EA SilentlyContinue;Write-Host 'Admin account created.'}catch{if($_.Exception.Message -like '*already exists*'){Write-Host 'Admin exists. Updating groups...';Add-LocalGroupMember -Group 'Administrators' -Member 'Admin' -EA SilentlyContinue;Add-LocalGroupMember -Group 'Remote Desktop Users' -Member 'Admin' -EA SilentlyContinue;Write-Host 'Groups updated.'}else{Write-Host "Error: $_"}}`);
                }
            },
            { text: 'Check Status', style: 'secondary', action: 'powershell', command: `try{$u=Get-LocalUser -Name 'Admin' -EA Stop;$g=Get-LocalGroup|Where-Object{(Get-LocalGroupMember $_ -EA SilentlyContinue).Name -like '*\\Admin'}|Select-Object -ExpandProperty Name;Write-Host "Admin account: EXISTS (Enabled: $($u.Enabled))";Write-Host "Groups: $($g -join ', ')"}catch{Write-Host 'Admin account: DOES NOT EXIST'}` }
        ]
    },
    {
        id: 'enable-rdp', name: 'Enable Remote Desktop', tags: ['network', 'security'],
        description: 'Enable Remote Desktop connections and configure firewall rules',
        buttons: [
            { text: 'Enable RDP', style: 'success', action: 'powershell', command: `Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server' -Name 'fDenyTSConnections' -Value 0 -Force;Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\\WinStations\\RDP-Tcp' -Name 'UserAuthentication' -Value 1 -Force;Enable-NetFirewallRule -DisplayGroup 'Remote Desktop' -EA SilentlyContinue;Write-Host 'Remote Desktop enabled with NLA.'` },
            { text: 'Disable RDP', style: 'danger', action: 'powershell', confirm: true, confirmTitle: 'Disable RDP', confirmDesc: 'This will disable Remote Desktop access.', command: `Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server' -Name 'fDenyTSConnections' -Value 1 -Force;Disable-NetFirewallRule -DisplayGroup 'Remote Desktop' -EA SilentlyContinue;Write-Host 'Remote Desktop disabled.'` },
            { text: 'Check Status', style: 'secondary', action: 'powershell', command: `$r=(Get-ItemProperty 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server' -Name 'fDenyTSConnections').fDenyTSConnections;$n=(Get-ItemProperty 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\\WinStations\\RDP-Tcp' -Name 'UserAuthentication' -EA SilentlyContinue).UserAuthentication;Write-Host "Remote Desktop: $(if($r -eq 0){'ENABLED'}else{'DISABLED'})";Write-Host "NLA: $(if($n -eq 1){'ENABLED'}else{'DISABLED'})"` }
        ]
    },
    // ═══ NEW TWEAKS ═══
    {
        id: 'windows-update', name: 'Windows Update Configuration', tags: ['system', 'security'],
        description: 'Configure Windows Update behavior (WinUtil-style: Default / Security / Disable)',
        buttons: [
            {
                text: '🔄 Default Settings', style: 'primary', action: 'powershell',
                confirm: true, confirmTitle: 'Reset Windows Update',
                confirmDesc: 'This resets your Windows Update settings to default out-of-box settings. It removes ANY policy or customization that has been made to Windows Update.',
                command: `
                    $wuPath='HKLM:\\\\SOFTWARE\\\\Policies\\\\Microsoft\\\\Windows\\\\WindowsUpdate'
                    $auPath='HKLM:\\\\SOFTWARE\\\\Policies\\\\Microsoft\\\\Windows\\\\WindowsUpdate\\\\AU'
                    if(Test-Path $auPath){Remove-Item $auPath -Recurse -Force -EA SilentlyContinue;Write-Host 'Removed AU policies'}
                    if(Test-Path $wuPath){
                        Remove-ItemProperty $wuPath -Name 'DeferFeatureUpdates' -EA SilentlyContinue
                        Remove-ItemProperty $wuPath -Name 'DeferFeatureUpdatesPeriodInDays' -EA SilentlyContinue
                        Remove-ItemProperty $wuPath -Name 'DeferQualityUpdates' -EA SilentlyContinue
                        Remove-ItemProperty $wuPath -Name 'DeferQualityUpdatesPeriodInDays' -EA SilentlyContinue
                        Write-Host 'Removed deferral policies'
                    }
                    $uxPath='HKLM:\\\\SOFTWARE\\\\Microsoft\\\\WindowsUpdate\\\\UX\\\\Settings'
                    @('PauseUpdatesExpiryTime','PauseFeatureUpdatesStartTime','PauseFeatureUpdatesEndTime','PauseQualityUpdatesStartTime','PauseQualityUpdatesEndTime')|ForEach-Object{Remove-ItemProperty $uxPath -Name $_ -EA SilentlyContinue}
                    Set-Service -Name wuauserv -StartupType Manual -EA SilentlyContinue
                    Start-Service -Name wuauserv -EA SilentlyContinue
                    Write-Host ''
                    Write-Host 'Windows Update reset to DEFAULT settings.'
                    Write-Host 'All custom policies removed. Updates will install normally.'
                `
            },
            {
                text: '🛡️ Security Settings', style: 'secondary', action: 'powershell',
                confirm: true, confirmTitle: 'Security Update Configuration',
                confirmDesc: 'Feature updates delayed by 365 days. Security updates installed after 4 days. Recommended for most users. Note: Only applies to Pro/Enterprise editions with Group Policy support.',
                command: `
                    $wuPath='HKLM:\\\\SOFTWARE\\\\Policies\\\\Microsoft\\\\Windows\\\\WindowsUpdate'
                    $auPath='HKLM:\\\\SOFTWARE\\\\Policies\\\\Microsoft\\\\Windows\\\\WindowsUpdate\\\\AU'
                    if(-not (Test-Path $wuPath)){New-Item -Path $wuPath -Force|Out-Null}
                    if(-not (Test-Path $auPath)){New-Item -Path $auPath -Force|Out-Null}
                    Set-ItemProperty $wuPath -Name 'DeferFeatureUpdates' -Value 1 -Type DWord -Force
                    Set-ItemProperty $wuPath -Name 'DeferFeatureUpdatesPeriodInDays' -Value 365 -Type DWord -Force
                    Set-ItemProperty $wuPath -Name 'DeferQualityUpdates' -Value 1 -Type DWord -Force
                    Set-ItemProperty $wuPath -Name 'DeferQualityUpdatesPeriodInDays' -Value 4 -Type DWord -Force
                    Set-ItemProperty $auPath -Name 'NoAutoUpdate' -Value 0 -Type DWord -Force
                    Set-ItemProperty $auPath -Name 'AUOptions' -Value 4 -Type DWord -Force
                    Set-Service -Name wuauserv -StartupType Manual -EA SilentlyContinue
                    Start-Service -Name wuauserv -EA SilentlyContinue
                    Write-Host ''
                    Write-Host 'Windows Update set to SECURITY mode.'
                    Write-Host 'Feature updates: delayed 365 days'
                    Write-Host 'Security updates: installed after 4 days'
                `
            },
            {
                text: '⛔ Disable All Updates', style: 'danger', action: 'powershell',
                confirm: true, confirmTitle: '⚠️ Disable ALL Windows Updates',
                confirmDesc: '!! NOT RECOMMENDED !! This disables ALL Windows Updates including security patches. Your system will be vulnerable. Only use for isolated/air-gapped systems.',
                command: `
                    $wuPath='HKLM:\\\\SOFTWARE\\\\Policies\\\\Microsoft\\\\Windows\\\\WindowsUpdate'
                    $auPath='HKLM:\\\\SOFTWARE\\\\Policies\\\\Microsoft\\\\Windows\\\\WindowsUpdate\\\\AU'
                    if(-not (Test-Path $wuPath)){New-Item -Path $wuPath -Force|Out-Null}
                    if(-not (Test-Path $auPath)){New-Item -Path $auPath -Force|Out-Null}
                    Set-ItemProperty $auPath -Name 'NoAutoUpdate' -Value 1 -Type DWord -Force
                    Set-ItemProperty $auPath -Name 'AUOptions' -Value 1 -Type DWord -Force
                    Stop-Service -Name wuauserv -Force -EA SilentlyContinue
                    Set-Service -Name wuauserv -StartupType Disabled -EA SilentlyContinue
                    Write-Host ''
                    Write-Host 'Windows Updates DISABLED.'
                    Write-Host 'WARNING: No security patches will be installed!'
                    Write-Host 'Run Default Settings to re-enable.'
                `
            },
            {
                text: '⏸️ Pause Updates (35 days)', style: 'secondary', action: 'powershell',
                confirm: true, confirmTitle: 'Pause Updates', confirmDesc: 'Pause ALL Windows Updates for 35 days?',
                command: `
                    $d=(Get-Date).AddDays(35).ToString('yyyy-MM-ddTHH:mm:ssZ')
                    $uxPath='HKLM:\\\\SOFTWARE\\\\Microsoft\\\\WindowsUpdate\\\\UX\\\\Settings'
                    Set-ItemProperty -Path $uxPath -Name 'PauseUpdatesExpiryTime' -Value $d -Force
                    Set-ItemProperty -Path $uxPath -Name 'PauseFeatureUpdatesStartTime' -Value (Get-Date -Format 'yyyy-MM-ddTHH:mm:ssZ') -Force
                    Set-ItemProperty -Path $uxPath -Name 'PauseFeatureUpdatesEndTime' -Value $d -Force
                    Set-ItemProperty -Path $uxPath -Name 'PauseQualityUpdatesStartTime' -Value (Get-Date -Format 'yyyy-MM-ddTHH:mm:ssZ') -Force
                    Set-ItemProperty -Path $uxPath -Name 'PauseQualityUpdatesEndTime' -Value $d -Force
                    Write-Host ''
                    Write-Host "Windows Updates PAUSED until $d"
                `
            },
            {
                text: '▶️ Resume Updates', style: 'secondary', action: 'powershell',
                command: `
                    $uxPath='HKLM:\\\\SOFTWARE\\\\Microsoft\\\\WindowsUpdate\\\\UX\\\\Settings'
                    @('PauseUpdatesExpiryTime','PauseFeatureUpdatesStartTime','PauseFeatureUpdatesEndTime','PauseQualityUpdatesStartTime','PauseQualityUpdatesEndTime')|ForEach-Object{Remove-ItemProperty $uxPath -Name $_ -EA SilentlyContinue}
                    Write-Host 'Windows Updates resumed.'
                `
            },
            {
                text: 'Check Status', style: 'secondary', action: 'powershell',
                command: `
                    Write-Host '=== Windows Update Configuration ==='
                    $wuPath='HKLM:\\\\SOFTWARE\\\\Policies\\\\Microsoft\\\\Windows\\\\WindowsUpdate'
                    $auPath='HKLM:\\\\SOFTWARE\\\\Policies\\\\Microsoft\\\\Windows\\\\WindowsUpdate\\\\AU'
                    $noAU=(Get-ItemProperty $auPath -Name 'NoAutoUpdate' -EA SilentlyContinue).NoAutoUpdate
                    $auOpt=(Get-ItemProperty $auPath -Name 'AUOptions' -EA SilentlyContinue).AUOptions
                    $deferFeat=(Get-ItemProperty $wuPath -Name 'DeferFeatureUpdatesPeriodInDays' -EA SilentlyContinue).DeferFeatureUpdatesPeriodInDays
                    $deferQual=(Get-ItemProperty $wuPath -Name 'DeferQualityUpdatesPeriodInDays' -EA SilentlyContinue).DeferQualityUpdatesPeriodInDays
                    $svc=Get-Service wuauserv -EA SilentlyContinue
                    Write-Host "Service: $($svc.Status) ($($svc.StartType))"
                    if($noAU -eq 1){Write-Host 'Mode: DISABLED (all updates off)';Write-Host 'WARNING: System is vulnerable!'}
                    elseif($deferFeat -gt 0){Write-Host "Mode: SECURITY";Write-Host "Feature defer: $deferFeat days";Write-Host "Quality defer: $deferQual days"}
                    else{Write-Host 'Mode: DEFAULT (no custom policies)'}
                    $exp=(Get-ItemProperty 'HKLM:\\\\SOFTWARE\\\\Microsoft\\\\WindowsUpdate\\\\UX\\\\Settings' -Name 'PauseUpdatesExpiryTime' -EA SilentlyContinue).PauseUpdatesExpiryTime
                    if($exp){Write-Host "Paused until: $exp"}
                `
            }
        ]
    },
    {
        id: 'startup-manager', name: 'Startup Programs Manager', tags: ['system', 'utility'],
        description: 'View and manage programs that run at startup',
        buttons: [
            {
                text: 'View Startup Items', style: 'primary', action: 'custom',
                handler: async () => { await showStartupViewDialog(); }
            },
            {
                text: '➕ Add Item', style: 'success', action: 'custom',
                handler: async () => {
                    const result = await showStartupAddDialog();
                    if (!result) return;
                    logToTerminal(`Adding startup item: ${result.name} → ${result.path}`, 'INFO');
                    await window.invokeX.runPowerShell(`Set-ItemProperty -Path 'HKCU:\\\\SOFTWARE\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run' -Name '${result.name.replace(/'/g, "''")}' -Value '"${result.path.replace(/'/g, "''")}"' -Force; Write-Host 'Added startup item: ${result.name}'`);
                }
            },
            {
                text: '➖ Remove Item', style: 'danger', action: 'custom',
                handler: async () => {
                    const name = await showStartupRemoveDialog();
                    if (!name) return;
                    const confirmed = await showConfirmDialog('Remove Startup Item', `Remove "${name}" from startup?`);
                    if (!confirmed) return;
                    logToTerminal(`Removing startup item: ${name}`, 'INFO');
                    await window.invokeX.runPowerShell(`Remove-ItemProperty -Path 'HKCU:\\\\SOFTWARE\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run' -Name '${name.replace(/'/g, "''")}' -Force -EA SilentlyContinue; Write-Host 'Removed startup item: ${name}'`);
                }
            },
            { text: 'Open Startup Folder', style: 'secondary', action: 'powershell', command: `Start-Process explorer.exe "$env:APPDATA\\\\Microsoft\\\\Windows\\\\Start Menu\\\\Programs\\\\Startup";Write-Host 'Startup folder opened.'` },
            { text: 'Open Task Manager', style: 'secondary', action: 'powershell', command: `Start-Process taskmgr.exe '/7';Write-Host 'Task Manager opened (Startup tab).'` }
        ]
    },
    {
        id: 'hosts-editor', name: 'Hosts File Editor', tags: ['network'],
        description: 'View and manage entries in the Windows hosts file',
        buttons: [
            { text: 'View Hosts File', style: 'primary', action: 'powershell', command: `$h=Get-Content "$env:SystemRoot\\System32\\drivers\\etc\\hosts" -EA SilentlyContinue;$entries=$h|Where-Object{$_ -and $_ -notmatch '^\\s*#'};Write-Host '=== Active Hosts Entries ===';if($entries){$entries|ForEach-Object{Write-Host $_}}else{Write-Host '(No custom entries)'}; Write-Host '';Write-Host "Total lines: $($h.Count) | Active entries: $($entries.Count)"` },
            { text: 'Open in Notepad', style: 'secondary', action: 'powershell', command: `Start-Process notepad.exe "$env:SystemRoot\\System32\\drivers\\etc\\hosts" -Verb RunAs -EA SilentlyContinue;Write-Host 'Hosts file opened in Notepad (as admin).'` },
            { text: 'Flush DNS', style: 'secondary', action: 'powershell', command: `ipconfig /flushdns;Write-Host 'DNS cache flushed successfully.'` }
        ]
    },
    {
        id: 'network-settings', name: 'Network Settings', tags: ['network'],
        description: 'DNS configuration, flush DNS, reset Winsock, view network info',
        buttons: [
            { text: 'Set Google DNS', style: 'primary', action: 'powershell', confirm: true, confirmTitle: 'Set Google DNS', confirmDesc: 'Set DNS servers to 8.8.8.8 and 8.8.4.4?', command: `$adapters=Get-NetAdapter|Where-Object{$_.Status -eq 'Up'};foreach($a in $adapters){Set-DnsClientServerAddress -InterfaceIndex $a.ifIndex -ServerAddresses ('8.8.8.8','8.8.4.4');Write-Host "Set Google DNS on: $($a.Name)"};ipconfig /flushdns;Write-Host 'DNS cache flushed.'` },
            { text: 'Reset Network', style: 'danger', action: 'powershell', confirm: true, confirmTitle: 'Reset Network Stack', confirmDesc: 'This will reset Winsock and IP configuration. Connection will be briefly interrupted.', command: `Write-Host 'Resetting Winsock...';netsh winsock reset;Write-Host 'Resetting IP config...';netsh int ip reset;Write-Host 'Flushing DNS...';ipconfig /flushdns;Write-Host 'Network stack reset. Restart may be required.'` },
            { text: 'View Network Info', style: 'secondary', action: 'powershell', command: `Get-NetAdapter|Where-Object{$_.Status -eq 'Up'}|ForEach-Object{$ip=Get-NetIPAddress -InterfaceIndex $_.ifIndex -AddressFamily IPv4 -EA SilentlyContinue;$dns=Get-DnsClientServerAddress -InterfaceIndex $_.ifIndex -AddressFamily IPv4 -EA SilentlyContinue;Write-Host "Adapter: $($_.Name) [$($_.LinkSpeed)]";Write-Host "  IP: $($ip.IPAddress)";Write-Host "  DNS: $($dns.ServerAddresses -join ', ')";Write-Host "  MAC: $($_.MacAddress)";Write-Host ''}` }
        ]
    },
    {
        id: 'defender-exclusion', name: 'Defender Exclusion for TRIP', tags: ['security'],
        description: 'Add/remove TRIP to Windows Defender exclusions to prevent false positive quarantine',
        buttons: [
            {
                text: '🛡️ Add Exclusion', style: 'primary', action: 'powershell',
                confirm: true, confirmTitle: 'Add Defender Exclusion',
                confirmDesc: 'This will add TRIP.exe paths to Windows Defender exclusions (process + folder).',
                command: `
                    $paths=@("$env:LOCALAPPDATA\\TRIP","$env:LOCALAPPDATA\\TRIP\\TRIP.exe","$env:USERPROFILE\\Desktop\\TRIP.exe","$env:USERPROFILE\\Downloads\\TRIP.exe")
                    $paths|ForEach-Object{Add-MpPreference -ExclusionPath $_ -EA SilentlyContinue;Write-Host "Added path exclusion: $_"}
                    Add-MpPreference -ExclusionProcess 'TRIP.exe' -EA SilentlyContinue
                    Write-Host 'Added process exclusion: TRIP.exe'
                    Write-Host ''
                    Write-Host 'TRIP exclusions added to Windows Defender.'
                `
            },
            {
                text: 'Remove Exclusion', style: 'secondary', action: 'powershell',
                command: `
                    $paths=@("$env:LOCALAPPDATA\\TRIP","$env:LOCALAPPDATA\\TRIP\\TRIP.exe","$env:USERPROFILE\\Desktop\\TRIP.exe","$env:USERPROFILE\\Downloads\\TRIP.exe")
                    $paths|ForEach-Object{Remove-MpPreference -ExclusionPath $_ -EA SilentlyContinue}
                    Remove-MpPreference -ExclusionProcess 'TRIP.exe' -EA SilentlyContinue
                    Write-Host 'TRIP exclusions removed from Windows Defender.'
                `
            },
            {
                text: 'Check Exclusions', style: 'secondary', action: 'powershell',
                command: `
                    Write-Host '=== Defender Exclusions ==='
                    $prefs=Get-MpPreference
                    Write-Host 'Path Exclusions:'
                    $prefs.ExclusionPath|ForEach-Object{Write-Host "  $_"}
                    Write-Host ''
                    Write-Host 'Process Exclusions:'
                    $prefs.ExclusionProcess|ForEach-Object{Write-Host "  $_"}
                `
            }
        ]
    }
];

// ──────────────────────────────────────────────
// Section 3: Toast Notifications
// ──────────────────────────────────────────────

const toastContainer = document.getElementById('toast-container');
function showToast(message, type = 'info') {
    const icons = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `<span class="toast-icon">${icons[type]}</span><span class="toast-message">${escapeHtml(message)}</span>`;
    toastContainer.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
}

// ──────────────────────────────────────────────
// Section 4: Terminal Logging
// ──────────────────────────────────────────────
// All output (PowerShell, downloads, errors) is logged to the
// collapsible terminal panel at the bottom of the window.

const terminalEl = document.getElementById('terminal-output');
const terminalPanel = document.getElementById('terminal-panel');

function logToTerminal(message, level = 'INFO') {
    const time = new Date().toLocaleTimeString('en-US', { hour12: false });
    const entry = document.createElement('div');
    entry.className = 'log-entry';
    entry.innerHTML = `<span class="log-time">${time}</span><span class="log-level ${level}">${level}</span><span class="log-separator">│</span><span class="log-message ${level}">${escapeHtml(message)}</span>`;
    terminalEl.appendChild(entry);
    terminalEl.scrollTop = terminalEl.scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

document.getElementById('clear-terminal-btn').addEventListener('click', () => {
    terminalEl.innerHTML = '';
    logToTerminal('Terminal cleared.', 'INFO');
});

// ──────────────────────────────────────────────
// Section 5: Terminal Expand / Collapse / Drag
// ──────────────────────────────────────────────

document.getElementById('expand-terminal-btn').addEventListener('click', () => {
    terminalPanel.classList.remove('collapsed');
    terminalPanel.classList.toggle('expanded');
    terminalPanel.style.height = '';
});

document.getElementById('collapse-terminal-btn').addEventListener('click', () => {
    terminalPanel.classList.remove('expanded');
    terminalPanel.style.height = '';
    terminalPanel.classList.toggle('collapsed');
});

const dragHandle = document.getElementById('terminal-drag-handle');
let isDragging = false, startY = 0, startHeight = 0;

dragHandle.addEventListener('mousedown', (e) => {
    isDragging = true; startY = e.clientY;
    startHeight = terminalPanel.getBoundingClientRect().height;
    terminalPanel.classList.remove('expanded', 'collapsed');
    terminalPanel.style.transition = 'none';
    dragHandle.classList.add('dragging');
    document.body.style.cursor = 'ns-resize';
    document.body.style.userSelect = 'none';
    e.preventDefault();
});

document.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    terminalPanel.style.height = Math.max(80, Math.min(window.innerHeight * 0.7, startHeight + (startY - e.clientY))) + 'px';
});

document.addEventListener('mouseup', () => {
    if (!isDragging) return;
    isDragging = false;
    terminalPanel.style.transition = '';
    dragHandle.classList.remove('dragging');
    document.body.style.cursor = '';
    document.body.style.userSelect = '';
});

// ──────────────────────────────────────────────
// Section 6: Results Popup (Structured Output Viewer)
// ──────────────────────────────────────────────
// When a tweak's output should be displayed in a popup table
// (e.g. View Startup Items, View Hosts File), capture the output
// and present it in a modal overlay.

const resultsOverlay = document.getElementById('results-overlay');
const resultsTitle = document.getElementById('results-title');
const resultsBody = document.getElementById('results-body');

function showResultsPopup(title, lines) {
    resultsTitle.textContent = title;
    resultsBody.innerHTML = '';
    const texts = lines.map(l => l.text);
    const tableData = parseTableOutput(texts);

    if (tableData) {
        const table = document.createElement('table');
        table.className = 'results-table';
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        tableData.headers.forEach(h => { const th = document.createElement('th'); th.textContent = h; headerRow.appendChild(th); });
        thead.appendChild(headerRow); table.appendChild(thead);
        const tbody = document.createElement('tbody');
        tableData.rows.forEach(row => {
            const tr = document.createElement('tr');
            row.forEach(cell => {
                const td = document.createElement('td'); td.textContent = cell;
                if (/error|failed/i.test(cell)) td.classList.add('cell-error');
                else if (/success|on|enabled|started/i.test(cell)) td.classList.add('cell-success');
                else if (/off|disabled|warning/i.test(cell)) td.classList.add('cell-warning');
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });
        table.appendChild(tbody); resultsBody.appendChild(table);
    } else {
        lines.forEach(({ text, level }) => {
            if (!text || !text.trim()) return;  // skip blank lines
            const lineEl = document.createElement('div');
            lineEl.className = 'results-line';

            // Key-value pairs (e.g. "IPv4 Address. . . . : 192.168.1.1")
            const kvMatch = text.match(/^([A-Za-z][A-Za-z0-9_ .]+?)\s*[.:]+\s*[:=]\s*(.+)$/) ||
                text.match(/^([A-Za-z][A-Za-z0-9_ ]+)\s*[:=]\s*(.+)$/);
            if (kvMatch) {
                lineEl.innerHTML = `<span class="results-key">${escapeHtml(kvMatch[1].trim().replace(/\.\s*\./g, ''))}</span><span class="results-value ${getValueClass(kvMatch[2])}">${escapeHtml(kvMatch[2].trim())}</span>`;
            } else if (/^(Ping statistics|Approximate round|Pinging |Tracing route|Trace complete|Windows IP Configuration|Ethernet adapter|Unknown adapter|Wireless LAN|Tunnel adapter)/i.test(text)) {
                // Section headers
                lineEl.classList.add('results-section-header');
                lineEl.textContent = text;
            } else {
                if (level === 'ERROR' || /error|failed|not found|Request timed out/i.test(text)) lineEl.classList.add('error-line');
                else if (level === 'SUCCESS' || /success|enabled|installed|exists|flushed/i.test(text)) lineEl.classList.add('success-line');
                else if (level === 'WARNING' || /warning|disabled|not set|not exist|unreachable/i.test(text)) lineEl.classList.add('warning-line');
                else if (/^(Packets|Minimum|Maximum)\b/i.test(text)) {
                    // Stats lines — split into key/value
                    const statMatch = text.match(/^(\w+)\s+(.+)$/);
                    if (statMatch) {
                        lineEl.innerHTML = `<span class="results-key">${escapeHtml(statMatch[1])}</span><span class="results-value">${escapeHtml(statMatch[2])}</span>`;
                    } else {
                        lineEl.textContent = text;
                    }
                } else {
                    lineEl.textContent = text;
                }
            }
            resultsBody.appendChild(lineEl);
        });
    }
    resultsOverlay.classList.remove('hidden');
}

function parseTableOutput(textLines) {
    let headerIdx = -1, dashIdx = -1;
    for (let i = 0; i < textLines.length - 1; i++) {
        if (/^[\s-]+$/.test(textLines[i + 1]) && textLines[i + 1].includes('-') && textLines[i + 1].trim().length > 3) { headerIdx = i; dashIdx = i + 1; break; }
    }
    if (headerIdx === -1) return null;
    const dashLine = textLines[dashIdx];
    const colRanges = []; let inDash = false, colStart = 0;
    for (let i = 0; i <= dashLine.length; i++) {
        const ch = i < dashLine.length ? dashLine[i] : ' ';
        if (ch === '-' && !inDash) { inDash = true; colStart = i; }
        else if (ch !== '-' && inDash) { inDash = false; colRanges.push([colStart, i]); }
    }
    if (colRanges.length === 0) return null;
    const headers = colRanges.map(([s, e]) => textLines[headerIdx].substring(s, Math.min(e, textLines[headerIdx].length)).trim());
    const rows = [];
    for (let i = dashIdx + 1; i < textLines.length; i++) {
        if (!textLines[i].trim()) continue;
        const cells = colRanges.map(([s, e], idx) => idx === colRanges.length - 1 ? textLines[i].substring(s).trim() : textLines[i].substring(s, Math.min(e, textLines[i].length)).trim());
        if (cells.some(c => c)) rows.push(cells);
    }
    return rows.length ? { headers, rows } : null;
}

function getValueClass(v) {
    if (/enabled|on|yes|true|exists|installed|success|running/i.test(v)) return 'value-success';
    if (/disabled|off|no|false|not|hidden|blocked/i.test(v)) return 'value-warning';
    if (/error|failed/i.test(v)) return 'value-error';
    return '';
}

function hideResultsPopup() { resultsOverlay.classList.add('hidden'); }
document.getElementById('results-close').addEventListener('click', hideResultsPopup);
document.getElementById('results-dismiss').addEventListener('click', hideResultsPopup);
resultsOverlay.addEventListener('click', (e) => { if (e.target === resultsOverlay) hideResultsPopup(); });

function shouldShowResults(btnText) { return /check|status|view|current/i.test(btnText); }

let capturedOutput = [], isCapturingOutput = false;

window.invokeX.onCommandOutput((data) => {
    data.text.split('\n').filter(l => l.trim()).forEach(line => {
        logToTerminal(line.trim(), data.level);
        if (isCapturingOutput) capturedOutput.push({ text: line.trim(), level: data.level });
    });
});

window.invokeX.onCommandComplete((data) => {
    const success = data.code === 0;
    logToTerminal(`Command completed (exit code: ${data.code})`, success ? 'SUCCESS' : 'WARNING');
});

// ──────────────────────────────────────────────
// Confirm Dialog
// ──────────────────────────────────────────────

function showConfirmDialog(title, desc) {
    return new Promise((resolve) => {
        const overlay = document.getElementById('confirm-overlay');
        document.getElementById('confirm-title').textContent = title;
        document.getElementById('confirm-desc').textContent = desc;
        overlay.classList.remove('hidden');
        const cleanup = (result) => { overlay.classList.add('hidden'); resolve(result); };
        document.getElementById('confirm-ok').onclick = () => cleanup(true);
        document.getElementById('confirm-cancel').onclick = () => cleanup(false);
        overlay.onclick = (e) => { if (e.target === overlay) cleanup(false); };
    });
}

// ──────────────────────────────────────────────
// Page Navigation
// ──────────────────────────────────────────────

const navItems = document.querySelectorAll('.nav-item');
const pages = document.querySelectorAll('.page');

function switchPage(target) {
    navItems.forEach(n => n.classList.toggle('active', n.dataset.page === target));
    pages.forEach(p => p.classList.toggle('active', p.id === `page-${target}`));
    // Auto-load system info on first visit
    if (target === 'system' && !sysInfoLoaded && typeof loadFullSystemInfo === 'function') {
        loadFullSystemInfo();
    }
}

navItems.forEach(item => item.addEventListener('click', () => switchPage(item.dataset.page)));

// ──────────────────────────────────────────────
// Search / Filter
// ──────────────────────────────────────────────

const searchInput = document.getElementById('search-input');
const searchClear = document.getElementById('search-clear');

searchInput.addEventListener('input', () => {
    const q = searchInput.value.toLowerCase().trim();
    searchClear.classList.toggle('visible', q.length > 0);

    document.querySelectorAll('.card').forEach(card => {
        const text = card.textContent.toLowerCase();
        card.classList.toggle('search-hidden', q.length > 0 && !text.includes(q));
    });

    // Show no-results message
    [document.getElementById('apps-grid'), document.getElementById('tweaks-grid')].forEach(grid => {
        const existing = grid.querySelector('.no-results');
        if (existing) existing.remove();
        const visible = grid.querySelectorAll('.card:not(.search-hidden)');
        if (q.length > 0 && visible.length === 0) {
            const msg = document.createElement('div');
            msg.className = 'no-results';
            msg.innerHTML = `<span class="no-results-icon">🔍</span>No results for "${escapeHtml(q)}"`;
            grid.appendChild(msg);
        }
    });
});

searchClear.addEventListener('click', () => {
    searchInput.value = '';
    searchInput.dispatchEvent(new Event('input'));
    searchInput.focus();
});

// ──────────────────────────────────────────────
// Theme Toggle
// ──────────────────────────────────────────────

const themeToggle = document.getElementById('theme-toggle');
let currentTheme = localStorage.getItem('invokex-theme') || 'dark';

function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    themeToggle.textContent = theme === 'dark' ? '🌙' : '☀️';
    currentTheme = theme;
    localStorage.setItem('invokex-theme', theme);
}

applyTheme(currentTheme);
themeToggle.addEventListener('click', () => applyTheme(currentTheme === 'dark' ? 'light' : 'dark'));

// ──────────────────────────────────────────────
// Batch Operations
// ──────────────────────────────────────────────

const batchBar = document.getElementById('batch-bar');
const batchCount = document.getElementById('batch-count');
const selectedApps = new Set();

function updateBatchBar() {
    if (selectedApps.size > 0) {
        batchBar.classList.remove('hidden');
        batchCount.textContent = `${selectedApps.size} selected`;
    } else {
        batchBar.classList.add('hidden');
    }
}

document.getElementById('batch-clear-btn').addEventListener('click', () => {
    selectedApps.clear();
    document.querySelectorAll('.card-checkbox.checked').forEach(cb => cb.classList.remove('checked'));
    updateBatchBar();
});

document.getElementById('batch-install-btn').addEventListener('click', async () => {
    const appsToInstall = APPS.filter(a => selectedApps.has(a.id));
    for (const app of appsToInstall) {
        const btn = app.buttons[0]; // First button is always install
        logToTerminal(`Batch installing: ${app.name}`, 'INFO');
        try {
            switch (btn.action) {
                case 'powershell': await window.invokeX.runPowerShell(btn.command); break;
                case 'exe': await window.invokeX.downloadAndInstallExe(btn.url, app.name); break;
                case 'portable': await window.invokeX.downloadPortable(btn.url, app.name); break;
                case 'msi': await window.invokeX.downloadAndInstallMsi(btn.url, app.name); break;
            }
            showToast(`${app.name} installed`, 'success');
        } catch (err) { showToast(`Failed: ${app.name}`, 'error'); }
    }
    selectedApps.clear();
    document.querySelectorAll('.card-checkbox.checked').forEach(cb => cb.classList.remove('checked'));
    updateBatchBar();
    showToast('Batch install complete', 'success');
});

// ──────────────────────────────────────────────
// Section 11: Render Application Cards
// ──────────────────────────────────────────────

/**
 * Render button HTML for a card. If there are more than 2 buttons,
 * only the first 2 are visible; the rest are hidden behind a
 * "More options ▾" toggle to keep card heights consistent.
 */
const MAX_VISIBLE_BUTTONS = 2;

function renderButtons(buttons) {
    if (buttons.length <= MAX_VISIBLE_BUTTONS) {
        return buttons.map((btn, i) => `<button class="btn btn-${btn.style}" data-btn="${i}">${escapeHtml(btn.text)}</button>`).join('');
    }
    const visible = buttons.slice(0, MAX_VISIBLE_BUTTONS);
    const hidden = buttons.slice(MAX_VISIBLE_BUTTONS);
    return `
        ${visible.map((btn, i) => `<button class="btn btn-${btn.style}" data-btn="${i}">${escapeHtml(btn.text)}</button>`).join('')}
        <button class="btn-expand-toggle" data-expanded="false">More options ▾</button>
        <div class="card-actions-hidden">
            ${hidden.map((btn, i) => `<button class="btn btn-${btn.style}" data-btn="${i + MAX_VISIBLE_BUTTONS}">${escapeHtml(btn.text)}</button>`).join('')}
        </div>
    `;
}

/**
 * Attach expand/collapse listeners to all toggle buttons in a card.
 */
function setupCardToggles(card) {
    const toggle = card.querySelector('.btn-expand-toggle');
    if (!toggle) return;
    toggle.addEventListener('click', () => {
        const hidden = card.querySelector('.card-actions-hidden');
        const isExpanded = toggle.dataset.expanded === 'true';
        toggle.dataset.expanded = isExpanded ? 'false' : 'true';
        toggle.textContent = isExpanded ? 'More options ▾' : 'Less options ▴';
        hidden.classList.toggle('expanded', !isExpanded);
    });
}

const appsGrid = document.getElementById('apps-grid');

function renderAppCard(app) {
    const card = document.createElement('div');
    card.className = 'card';
    card.id = `card-${app.id}`;
    card.dataset.appId = app.id;
    const statusId = `status-${app.id}`;
    const progressId = `progress-${app.id}`;

    const tagsHtml = (app.tags || []).map(t => `<span class="card-tag tag-${t}">${t}</span>`).join('');

    card.innerHTML = `
    <div class="card-checkbox" data-app-id="${app.id}" title="Select for batch install">✓</div>
    <div class="card-header">
      <div class="card-title-group">
        <div class="card-title">${escapeHtml(app.name)}</div>
        <div class="card-desc">${escapeHtml(app.description)}</div>
      </div>
      <div class="card-status checking" id="${statusId}"><span>⏳</span> Checking...</div>
    </div>
    <div class="card-tags">${tagsHtml}</div>
    <button class="card-link" data-url="${app.url}">🔗 ${app.url.includes('github') ? 'GitHub' : 'Website'}</button>
    <div class="card-actions">
      ${renderButtons(app.buttons)}
    </div>
    <div class="progress-bar-container" id="${progressId}"><div class="progress-bar"></div></div>
  `;

    // Checkbox
    card.querySelector('.card-checkbox').addEventListener('click', (e) => {
        e.stopPropagation();
        const cb = e.currentTarget;
        if (selectedApps.has(app.id)) { selectedApps.delete(app.id); cb.classList.remove('checked'); }
        else { selectedApps.add(app.id); cb.classList.add('checked'); }
        updateBatchBar();
    });

    card.querySelector('.card-link').addEventListener('click', () => window.invokeX.openUrl(app.url));
    card.querySelectorAll('.btn').forEach(btn => {
        const btnDef = app.buttons[parseInt(btn.dataset.btn)];
        btn.addEventListener('click', () => handleAction(btnDef, app, btn));
    });
    setupCardToggles(card);

    appsGrid.appendChild(card);
    checkAppStatus(app, statusId);
}

async function checkAppStatus(app, statusId) {
    const el = document.getElementById(statusId);
    if (!el) return;
    if (app.alwaysAvailable) { el.className = 'card-status installed'; el.innerHTML = '<span>✅</span> Available'; return; }
    try {
        const installed = await window.invokeX.checkAppInstalled(app.checkName);
        const prev = el.classList.contains('installed');
        el.className = installed ? 'card-status installed' : 'card-status not-installed';
        el.innerHTML = installed ? '<span>✅</span> Installed' : '<span>○</span> Not installed';
        if (installed !== prev) { el.classList.add('just-changed'); setTimeout(() => el.classList.remove('just-changed'), 600); }
    } catch { el.className = 'card-status not-installed'; el.innerHTML = '<span>○</span> Unknown'; }
}

// ──────────────────────────────────────────────
// Render Tweak Cards
// ──────────────────────────────────────────────

const tweaksGrid = document.getElementById('tweaks-grid');

function renderTweakCard(tweak) {
    const card = document.createElement('div');
    card.className = 'card';
    card.id = `card-${tweak.id}`;
    const tagsHtml = (tweak.tags || []).map(t => `<span class="card-tag tag-${t}">${t}</span>`).join('');

    card.innerHTML = `
    <div class="card-header">
      <div class="card-title-group">
        <div class="card-title">${escapeHtml(tweak.name)}</div>
        <div class="card-desc">${escapeHtml(tweak.description)}</div>
      </div>
    </div>
    <div class="card-tags">${tagsHtml}</div>
    <div class="card-actions">
      ${renderButtons(tweak.buttons)}
    </div>
  `;

    card.querySelectorAll('.btn').forEach(btn => {
        const btnDef = tweak.buttons[parseInt(btn.dataset.btn)];
        btn.addEventListener('click', () => handleAction(btnDef, tweak, btn));
    });
    setupCardToggles(card);

    tweaksGrid.appendChild(card);
}

// ──────────────────────────────────────────────
// Action Handler
// ──────────────────────────────────────────────

async function handleAction(btnDef, item, btnEl) {
    // Confirmation dialog for destructive actions
    if (btnDef.confirm) {
        const ok = await showConfirmDialog(btnDef.confirmTitle || 'Confirm', btnDef.confirmDesc || 'Are you sure?');
        if (!ok) return;
    }

    btnEl.disabled = true;
    btnEl.classList.add('loading');
    const originalText = btnEl.textContent;
    logToTerminal(`Executing: ${item.name} → ${btnDef.text}`, 'INFO');

    const showPopup = shouldShowResults(btnDef.text);
    if (showPopup) { capturedOutput = []; isCapturingOutput = true; }

    try {
        switch (btnDef.action) {
            case 'powershell':
            case 'powershell-stream':
                await window.invokeX.runPowerShell(btnDef.command);
                if (!showPopup) showToast(`${item.name}: ${btnDef.text} completed`, 'success');
                break;
            case 'powershell-window':
                await window.invokeX.runPowerShellWindow(btnDef.command);
                showToast(`${item.name} launched in a new window`, 'success');
                break;
            case 'exe':
                await window.invokeX.downloadAndInstallExe(btnDef.url, item.name);
                showToast(`${item.name} installed`, 'success');
                if (item.checkName) setTimeout(() => checkAppStatus(item, `status-${item.id}`), 3000);
                break;
            case 'portable':
                await window.invokeX.downloadPortable(btnDef.url, item.name);
                showToast(`${item.name} saved to Desktop`, 'success');
                if (item.checkName) setTimeout(() => checkAppStatus(item, `status-${item.id}`), 3000);
                break;
            case 'msi':
                await window.invokeX.downloadAndInstallMsi(btnDef.url, item.name);
                showToast(`${item.name} installed`, 'success');
                if (item.checkName) setTimeout(() => checkAppStatus(item, `status-${item.id}`), 3000);
                break;
            case 'custom':
                if (btnDef.handler) await btnDef.handler();
                break;
        }
    } catch (err) {
        logToTerminal(`Error: ${err.message || err}`, 'ERROR');
        showToast(`Error: ${err.message || err}`, 'error');
        if (showPopup) capturedOutput.push({ text: `Error: ${err.message || err}`, level: 'ERROR' });
    } finally {
        btnEl.disabled = false;
        btnEl.classList.remove('loading');
        btnEl.textContent = originalText;
        if (showPopup) {
            isCapturingOutput = false;
            if (capturedOutput.length > 0) showResultsPopup(`${item.name} — ${btnDef.text}`, capturedOutput);
        }
    }
}

// ──────────────────────────────────────────────
// Password Dialog
// ──────────────────────────────────────────────

function showPasswordDialog() {
    return new Promise((resolve) => {
        const overlay = document.createElement('div');
        overlay.className = 'dialog-overlay';
        overlay.innerHTML = `
      <div class="dialog-box">
        <div class="dialog-title">Create Admin Account</div>
        <div class="dialog-desc">Enter a password for the new Admin account. Must be at least 8 characters.</div>
        <input type="password" class="dialog-input" id="dialog-password" placeholder="Password" autocomplete="new-password">
        <input type="password" class="dialog-input" id="dialog-password-confirm" placeholder="Confirm password" autocomplete="new-password">
        <div class="dialog-input-hint">Password must meet Windows complexity requirements.</div>
        <div class="dialog-actions">
          <button class="btn btn-secondary" id="dialog-cancel">Cancel</button>
          <button class="btn btn-primary" id="dialog-ok">Create Account</button>
        </div>
      </div>`;
        document.body.appendChild(overlay);
        const pwIn = document.getElementById('dialog-password');
        const cfIn = document.getElementById('dialog-password-confirm');
        pwIn.focus();
        document.getElementById('dialog-cancel').onclick = () => { overlay.remove(); resolve(null); };
        document.getElementById('dialog-ok').onclick = () => {
            if (pwIn.value.length < 8) { pwIn.style.borderColor = 'var(--error)'; return; }
            if (pwIn.value !== cfIn.value) { cfIn.style.borderColor = 'var(--error)'; return; }
            overlay.remove(); resolve(pwIn.value);
        };
        [pwIn, cfIn].forEach(el => el.addEventListener('keydown', e => { if (e.key === 'Enter') document.getElementById('dialog-ok').click(); }));
        overlay.addEventListener('click', e => { if (e.target === overlay) { overlay.remove(); resolve(null); } });
    });
}

// ──────────────────────────────────────────────
// Startup Manager Dialogs
// ──────────────────────────────────────────────

async function showStartupViewDialog() {
    const overlay = document.createElement('div');
    overlay.className = 'dialog-overlay';
    overlay.innerHTML = `
      <div class="dialog-box" style="max-width:600px;width:90%">
        <div class="dialog-title">Startup Programs Manager</div>
        <div class="dialog-desc">Loading startup items...</div>
        <div id="startup-view-list" style="max-height:400px;overflow-y:auto;margin:8px 0"></div>
        <div class="dialog-actions">
          <button class="btn btn-secondary" id="startup-view-close">Close</button>
        </div>
      </div>`;
    document.body.appendChild(overlay);
    document.getElementById('startup-view-close').onclick = () => overlay.remove();
    overlay.addEventListener('click', e => { if (e.target === overlay) overlay.remove(); });

    async function loadItems() {
        const listEl = document.getElementById('startup-view-list');
        const descEl = overlay.querySelector('.dialog-desc');
        listEl.innerHTML = '<div style="text-align:center;color:var(--text-muted);padding:16px">Loading...</div>';

        const entryCountBefore = terminalEl.querySelectorAll('.log-message').length;
        await window.invokeX.runPowerShell(`
            $reg=Get-ItemProperty 'HKCU:\\\\SOFTWARE\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run' -EA SilentlyContinue
            if($reg){$reg.PSObject.Properties|Where-Object{$_.Name -notlike 'PS*'}|ForEach-Object{Write-Host "SVIEW|REG|$($_.Name)|$($_.Value)"}}
            $folder="$env:APPDATA\\\\Microsoft\\\\Windows\\\\Start Menu\\\\Programs\\\\Startup"
            if(Test-Path $folder){Get-ChildItem $folder -EA SilentlyContinue|ForEach-Object{Write-Host "SVIEW|FOLDER|$($_.Name)|$($_.FullName)"}}
        `);

        setTimeout(() => {
            const items = [];
            const allEntries = terminalEl.querySelectorAll('.log-message');
            for (let i = entryCountBefore; i < allEntries.length; i++) {
                const text = allEntries[i].textContent;
                if (text.startsWith('SVIEW|')) {
                    const parts = text.split('|');
                    items.push({ source: parts[1], name: parts[2], path: parts[3] || '' });
                }
            }

            if (items.length === 0) {
                descEl.textContent = 'No startup items found.';
                listEl.innerHTML = '';
                return;
            }
            descEl.textContent = `${items.length} startup items found:`;
            listEl.innerHTML = items.map((item, idx) =>
                `<div class="startup-view-item" data-idx="${idx}" style="display:flex;align-items:center;justify-content:space-between;padding:10px 12px;margin:4px 0;background:var(--bg-tertiary);border-radius:var(--radius-sm);gap:12px">
                    <div style="flex:1;min-width:0">
                        <div style="display:flex;align-items:center;gap:6px">
                            <strong style="color:var(--text-primary)">${escapeHtml(item.name)}</strong>
                            <span style="font-size:10px;padding:1px 6px;border-radius:3px;background:${item.source === 'REG' ? 'var(--accent)' : 'var(--warning)'};color:#000;font-weight:600">${item.source === 'REG' ? 'Registry' : 'Folder'}</span>
                        </div>
                        <div style="font-size:11px;color:var(--text-muted);margin-top:2px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${escapeHtml(item.path)}</div>
                    </div>
                    <button class="btn btn-danger startup-remove-btn" data-source="${item.source}" data-name="${escapeHtml(item.name)}" data-path="${escapeHtml(item.path)}" style="padding:4px 10px;font-size:12px;flex-shrink:0">✕ Remove</button>
                </div>`
            ).join('');

            listEl.querySelectorAll('.startup-remove-btn').forEach(btn => {
                btn.addEventListener('click', async (e) => {
                    e.stopPropagation();
                    const itemName = btn.dataset.name;
                    const source = btn.dataset.source;
                    const confirmed = await showConfirmDialog('Remove Startup Item', `Remove "${itemName}" from startup?`);
                    if (!confirmed) return;
                    if (source === 'REG') {
                        await window.invokeX.runPowerShell(`Remove-ItemProperty -Path 'HKCU:\\\\SOFTWARE\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run' -Name '${itemName.replace(/'/g, "''")}' -Force -EA SilentlyContinue; Write-Host 'Removed: ${itemName}'`);
                    } else {
                        const itemPath = btn.dataset.path;
                        await window.invokeX.runPowerShell(`Remove-Item '${itemPath.replace(/'/g, "''")}' -Force -EA SilentlyContinue; Write-Host 'Removed: ${itemName}'`);
                    }
                    logToTerminal(`Removed startup item: ${itemName}`, 'SUCCESS');
                    showToast(`Removed "${itemName}" from startup`, 'success');
                    // Refresh the list
                    await loadItems();
                });
            });
        }, 2000);
    }

    await loadItems();
}

function showStartupAddDialog() {
    return new Promise((resolve) => {
        const overlay = document.createElement('div');
        overlay.className = 'dialog-overlay';
        overlay.innerHTML = `
      <div class="dialog-box">
        <div class="dialog-title">Add Startup Item</div>
        <div class="dialog-desc">Enter a name and select the executable to run at startup.</div>
        <input type="text" class="dialog-input" id="startup-name" placeholder="Name (e.g. MyApp)" autocomplete="off">
        <div style="display:flex;gap:6px;align-items:center">
          <input type="text" class="dialog-input" id="startup-path" placeholder="Path to executable" style="flex:1;margin:0" autocomplete="off" readonly>
          <button class="btn btn-secondary" id="startup-browse" style="white-space:nowrap">Browse</button>
        </div>
        <div class="dialog-actions">
          <button class="btn btn-secondary" id="startup-cancel">Cancel</button>
          <button class="btn btn-primary" id="startup-ok">Add to Startup</button>
        </div>
      </div>`;
        document.body.appendChild(overlay);
        const nameIn = document.getElementById('startup-name');
        const pathIn = document.getElementById('startup-path');
        nameIn.focus();
        document.getElementById('startup-browse').onclick = async () => {
            const file = await window.invokeX.browseForFile('Select executable');
            if (file) pathIn.value = file;
        };
        document.getElementById('startup-cancel').onclick = () => { overlay.remove(); resolve(null); };
        document.getElementById('startup-ok').onclick = () => {
            if (!nameIn.value.trim()) { nameIn.style.borderColor = 'var(--error)'; return; }
            if (!pathIn.value.trim()) { pathIn.style.borderColor = 'var(--error)'; return; }
            overlay.remove();
            resolve({ name: nameIn.value.trim(), path: pathIn.value.trim() });
        };
        nameIn.addEventListener('keydown', e => { if (e.key === 'Enter') document.getElementById('startup-ok').click(); });
        overlay.addEventListener('click', e => { if (e.target === overlay) { overlay.remove(); resolve(null); } });
    });
}

function showStartupRemoveDialog() {
    return new Promise(async (resolve) => {
        const overlay = document.createElement('div');
        overlay.className = 'dialog-overlay';
        overlay.innerHTML = `
      <div class="dialog-box">
        <div class="dialog-title">Remove Startup Item</div>
        <div class="dialog-desc">Loading startup items...</div>
        <div id="startup-list" style="max-height:300px;overflow-y:auto;margin:8px 0"></div>
        <div class="dialog-actions">
          <button class="btn btn-secondary" id="startup-remove-cancel">Cancel</button>
        </div>
      </div>`;
        document.body.appendChild(overlay);
        document.getElementById('startup-remove-cancel').onclick = () => { overlay.remove(); resolve(null); };
        overlay.addEventListener('click', e => { if (e.target === overlay) { overlay.remove(); resolve(null); } });

        // Fetch startup items from registry
        try {
            const entryCountBefore = terminalEl.querySelectorAll('.log-message').length;
            await window.invokeX.runPowerShell(`$items=(Get-ItemProperty 'HKCU:\\\\SOFTWARE\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run' -EA SilentlyContinue);$items.PSObject.Properties|Where-Object{$_.Name -notlike 'PS*'}|ForEach-Object{Write-Host "STARTUPITEM|$($_.Name)|$($_.Value)"}`);

            setTimeout(() => {
                const items = [];
                const allEntries = terminalEl.querySelectorAll('.log-message');
                for (let i = entryCountBefore; i < allEntries.length; i++) {
                    const text = allEntries[i].textContent;
                    if (text.startsWith('STARTUPITEM|')) {
                        const parts = text.split('|');
                        items.push({ name: parts[1], path: parts[2] || '' });
                    }
                }

                const listEl = document.getElementById('startup-list');
                const descEl = overlay.querySelector('.dialog-desc');
                if (items.length === 0) {
                    descEl.textContent = 'No startup items found in the current user registry.';
                    return;
                }
                descEl.textContent = 'Click an item to remove it:';
                listEl.innerHTML = items.map(item =>
                    `<div class="startup-list-item" data-name="${escapeHtml(item.name)}" style="padding:8px 12px;margin:4px 0;background:var(--bg-tertiary);border-radius:var(--radius-sm);cursor:pointer;display:flex;justify-content:space-between;align-items:center;transition:background 0.15s">
                        <div><strong style="color:var(--text-primary)">${escapeHtml(item.name)}</strong><br><span style="font-size:11px;color:var(--text-muted)">${escapeHtml(item.path)}</span></div>
                        <span style="color:var(--error);font-size:18px">✕</span>
                    </div>`
                ).join('');

                listEl.querySelectorAll('.startup-list-item').forEach(el => {
                    el.addEventListener('mouseenter', () => el.style.background = 'var(--bg-hover)');
                    el.addEventListener('mouseleave', () => el.style.background = 'var(--bg-tertiary)');
                    el.addEventListener('click', () => {
                        overlay.remove();
                        resolve(el.dataset.name);
                    });
                });
            }, 2000);
        } catch (err) {
            logToTerminal(`Error loading startup items: ${err}`, 'ERROR');
            overlay.remove();
            resolve(null);
        }
    });
}

// ──────────────────────────────────────────────
// Download Progress
// ──────────────────────────────────────────────

window.invokeX.onDownloadProgress((data) => {
    const app = APPS.find(a => a.name === data.appName);
    if (app) {
        const container = document.getElementById(`progress-${app.id}`);
        if (container) {
            container.classList.add('active');
            container.querySelector('.progress-bar').style.width = `${data.percent}%`;
            if (data.percent >= 100) setTimeout(() => container.classList.remove('active'), 2000);
        }
    }
});

// ──────────────────────────────────────────────
// Sidebar Shortcut Buttons
// ──────────────────────────────────────────────

document.getElementById('shortcut-controlpanel').addEventListener('click', async () => {
    await window.invokeX.runPowerShell("Start-Process control.exe; Write-Host 'Control Panel opened.'");
    showToast('Control Panel opened', 'info');
});

document.getElementById('shortcut-settings').addEventListener('click', async () => {
    await window.invokeX.runPowerShell("Start-Process ms-settings:; Write-Host 'Settings opened.'");
    showToast('Windows Settings opened', 'info');
});

document.getElementById('shortcut-terminal').addEventListener('click', async () => {
    await window.invokeX.runPowerShell("Start-Process wt.exe; Write-Host 'Windows Terminal opened.'");
    showToast('Windows Terminal opened', 'info');
});

document.getElementById('shortcut-reboot').addEventListener('click', async () => {
    const ok = await showConfirmDialog('Restart PC', 'Are you sure you want to restart this computer? All unsaved work will be lost.');
    if (!ok) return;
    logToTerminal('Restarting PC...', 'WARNING');
    await window.invokeX.runPowerShell("shutdown /r /t 0");
});

// ──────────────────────────────────────────────
// Keyboard Shortcuts
// ──────────────────────────────────────────────

document.addEventListener('keydown', (e) => {
    // Ctrl+K: Focus search
    if (e.ctrlKey && e.key === 'k') { e.preventDefault(); searchInput.focus(); searchInput.select(); }
    // Ctrl+1: Applications tab
    if (e.ctrlKey && e.key === '1') { e.preventDefault(); switchPage('apps'); }
    // Ctrl+2: System Tweaks tab
    if (e.ctrlKey && e.key === '2') { e.preventDefault(); switchPage('tweaks'); }
    // Ctrl+3: Network Tools tab
    if (e.ctrlKey && e.key === '3') { e.preventDefault(); switchPage('nettools'); }
    // Ctrl+4: Net Diagnostics tab
    if (e.ctrlKey && e.key === '4') { e.preventDefault(); switchPage('netdiag'); }
    // Ctrl+5: System tab
    if (e.ctrlKey && e.key === '5') { e.preventDefault(); switchPage('system'); }
    // Ctrl+T: Toggle theme
    if (e.ctrlKey && e.key === 't') { e.preventDefault(); applyTheme(currentTheme === 'dark' ? 'light' : 'dark'); }
    // Ctrl+`: Toggle terminal
    if (e.ctrlKey && e.key === '`') { e.preventDefault(); terminalPanel.classList.toggle('expanded'); terminalPanel.classList.remove('collapsed'); terminalPanel.style.height = ''; }
    // Escape: Close popups/clear search
    if (e.key === 'Escape') {
        if (!resultsOverlay.classList.contains('hidden')) hideResultsPopup();
        else if (searchInput.value) { searchInput.value = ''; searchInput.dispatchEvent(new Event('input')); }
        else if (document.activeElement === searchInput) searchInput.blur();
    }
});

// ──────────────────────────────────────────────
// System Info
// ──────────────────────────────────────────────

async function loadSystemInfo() {
    const infoEl = document.getElementById('system-info');
    if (!infoEl) return;
    try {
        const info = await window.invokeX.runPowerShell(`
      $cpu=(Get-CimInstance Win32_Processor).Name -replace '\\s+',' ';
      $ram=[math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory/1GB,1);
      $disk=Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'";
      $diskFree=[math]::Round($disk.FreeSpace/1GB,1);
      $diskTotal=[math]::Round($disk.Size/1GB,1);
      $ip=(Get-NetIPAddress -AddressFamily IPv4|Where-Object{$_.InterfaceAlias -notlike '*Loopback*' -and $_.PrefixOrigin -ne 'WellKnown'}|Select-Object -First 1).IPAddress;
      $uptime=(Get-Date)-(Get-CimInstance Win32_OperatingSystem).LastBootUpTime;
      $uptimeStr='{0}d {1}h {2}m' -f $uptime.Days,$uptime.Hours,$uptime.Minutes;
      Write-Host "CPU|$cpu";
      Write-Host "RAM|$ram GB";
      Write-Host "Disk (C:)|$diskFree / $diskTotal GB free";
      Write-Host "IP|$ip";
      Write-Host "Uptime|$uptimeStr";
    `);
    } catch { }

    // Parse from captured terminal output after a delay
    setTimeout(() => {
        const entries = [];
        const logEntries = terminalEl.querySelectorAll('.log-message');
        logEntries.forEach(el => {
            const text = el.textContent;
            if (text.includes('|') && ['CPU', 'RAM', 'Disk', 'IP', 'Uptime'].some(k => text.startsWith(k))) {
                const [label, value] = text.split('|');
                entries.push({ label: label.trim(), value: value.trim() });
            }
        });

        if (entries.length > 0) {
            infoEl.innerHTML = entries.map(e =>
                `<div class="sys-info-row"><span class="sys-info-label">${escapeHtml(e.label)}</span><span class="sys-info-value">${escapeHtml(e.value)}</span></div>`
            ).join('');
        }
    }, 3000);
}

// ──────────────────────────────────────────────
// System Info Dashboard (Full Page)
// ──────────────────────────────────────────────

let sysInfoLoaded = false;

async function loadFullSystemInfo() {
    const loading = document.getElementById('sysinfo-loading');
    const grid = document.getElementById('sysinfo-grid');
    loading.classList.remove('hidden');
    grid.classList.add('hidden');

    // Snapshot current terminal entry count so we only parse NEW entries
    const terminalEntriesBefore = terminalEl.querySelectorAll('.log-message').length;

    try {
        await window.invokeX.runPowerShell(`
            # OS
            $os=Get-CimInstance Win32_OperatingSystem
            Write-Host "OS|Name|$($os.Caption)"
            Write-Host "OS|Version|$($os.Version)"
            Write-Host "OS|Build|$($os.BuildNumber)"
            Write-Host "OS|Architecture|$($os.OSArchitecture)"

            # CPU
            $cpus=@(Get-CimInstance Win32_Processor)
            $cpuCount=$cpus.Count
            Write-Host "CPU|Processors|$cpuCount"
            $totalCores=0;$totalThreads=0
            $idx=0
            foreach($c in $cpus){
                $idx++
                $prefix=$(if($cpuCount -gt 1){"CPU $idx"}else{"Name"})
                Write-Host "CPU|$prefix|$($c.Name -replace '\\s+',' ')"
                $totalCores+=$c.NumberOfCores
                $totalThreads+=$c.NumberOfLogicalProcessors
            }
            Write-Host "CPU|Cores|$totalCores cores / $totalThreads threads"
            Write-Host "CPU|Max Speed|$($cpus[0].MaxClockSpeed) MHz"

            # RAM
            $cs=Get-CimInstance Win32_ComputerSystem
            $totalRAM=[math]::Round($cs.TotalPhysicalMemory/1GB,1)
            $osRAM=[math]::Round(($os.TotalVisibleMemorySize - $os.FreePhysicalMemory)/1KB/1024,1)
            $freeRAM=[math]::Round($os.FreePhysicalMemory/1KB/1024,1)
            Write-Host "RAM|Total|$totalRAM GB"
            Write-Host "RAM|Used|$osRAM GB"
            Write-Host "RAM|Free|$freeRAM GB"

            # Storage — ALL drives
            $disks=Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3"
            foreach($d in $disks){
                $total=[math]::Round($d.Size/1GB,1)
                $free=[math]::Round($d.FreeSpace/1GB,1)
                $used=[math]::Round(($d.Size-$d.FreeSpace)/1GB,1)
                $pct=$(if($d.Size -gt 0){[math]::Round(($d.Size-$d.FreeSpace)/$d.Size*100,0)}else{0})
                $label=$d.DeviceID
                if($d.VolumeName){$label="$($d.DeviceID) $($d.VolumeName)"}
                Write-Host "STORAGE|$label|$used/$total GB used ($free GB free)|$pct"
            }

            # GPU
            $gpus=Get-CimInstance Win32_VideoController
            foreach($g in $gpus){
                $vramVal=$(if($g.AdapterRAM -gt 0){[math]::Round($g.AdapterRAM/1MB)}else{0})
                Write-Host "GPU|$($g.Name)|$($vramVal)MB VRAM"
            }

            # Motherboard
            $mb=Get-CimInstance Win32_BaseBoard
            Write-Host "MOBO|Manufacturer|$($mb.Manufacturer)"
            Write-Host "MOBO|Product|$($mb.Product)"

            # Network
            $adapters=Get-NetAdapter|Where-Object{$_.Status -eq 'Up'}
            foreach($a in $adapters){
                $ip=(Get-NetIPAddress -InterfaceIndex $a.ifIndex -AddressFamily IPv4 -EA SilentlyContinue).IPAddress
                if($ip){Write-Host "NET|$($a.Name)|$ip ($($a.LinkSpeed))"}
            }
            try{$ext=(Invoke-RestMethod -Uri 'https://api.ipify.org' -TimeoutSec 5);Write-Host "NET|External IP|$ext"}catch{Write-Host "NET|External IP|Unavailable"}

            # Uptime
            $uptime=(Get-Date)-$os.LastBootUpTime
            Write-Host "UPTIME|Uptime|$($uptime.Days)d $($uptime.Hours)h $($uptime.Minutes)m"
            Write-Host "UPTIME|Last Boot|$($os.LastBootUpTime.ToString('yyyy-MM-dd HH:mm:ss'))"
        `);
    } catch (err) {
        logToTerminal(`System info error: ${err}`, 'ERROR');
    }

    // Parse terminal output after delay
    setTimeout(() => {
        const data = { OS: [], CPU: [], RAM: [], STORAGE: [], GPU: [], MOBO: [], NET: [], UPTIME: [] };
        const allEntries = terminalEl.querySelectorAll('.log-message');
        // Only parse entries added AFTER the PowerShell started
        for (let i = terminalEntriesBefore; i < allEntries.length; i++) {
            const text = allEntries[i].textContent;
            const parts = text.split('|');
            if (parts.length >= 3) {
                const section = parts[0].trim();
                if (data[section] !== undefined) {
                    data[section].push({ key: parts[1].trim(), value: parts[2].trim(), extra: parts[3]?.trim() });
                }
            }
        }

        // Helper for key-value rows
        const renderRow = (label, value, highlight) =>
            `<div class="sysinfo-row"><span class="sysinfo-label">${escapeHtml(label)}</span><span class="sysinfo-value ${highlight ? 'highlight' : ''}">${escapeHtml(value)}</span></div>`;

        // OS + Uptime (merged)
        const osEl = document.getElementById('sysinfo-os');
        if (data.OS.length || data.UPTIME.length) {
            const osRows = data.OS.map(r => renderRow(r.key, r.value)).join('');
            const uptimeRows = data.UPTIME.map(r => renderRow(r.key, r.value, r.key === 'Uptime')).join('');
            osEl.innerHTML = osRows + uptimeRows;
        }

        // CPU
        const cpuEl = document.getElementById('sysinfo-cpu');
        if (data.CPU.length) cpuEl.innerHTML = data.CPU.map(r => renderRow(r.key, r.value)).join('');

        // RAM
        const ramEl = document.getElementById('sysinfo-ram');
        if (data.RAM.length) ramEl.innerHTML = data.RAM.map(r => renderRow(r.key, r.value, r.key === 'Total')).join('');

        // Storage — render with bars
        const storageEl = document.getElementById('sysinfo-storage');
        if (data.STORAGE.length) {
            storageEl.innerHTML = data.STORAGE.map(r => {
                const pct = parseInt(r.extra) || 0;
                const fillClass = pct > 90 ? 'danger' : pct > 75 ? 'warning' : '';
                return `<div class="sysinfo-drive">
                    <div class="sysinfo-drive-header">
                        <span class="sysinfo-drive-label">${escapeHtml(r.key)}</span>
                        <span class="sysinfo-drive-space">${escapeHtml(r.value)}</span>
                    </div>
                    <div class="sysinfo-drive-bar">
                        <div class="sysinfo-drive-fill ${fillClass}" style="width:${pct}%"></div>
                    </div>
                </div>`;
            }).join('');
        }

        // GPU
        const gpuEl = document.getElementById('sysinfo-gpu');
        if (data.GPU.length) gpuEl.innerHTML = data.GPU.map(r => renderRow(r.key, r.value)).join('');

        // Motherboard
        const moboEl = document.getElementById('sysinfo-mobo');
        if (data.MOBO.length) moboEl.innerHTML = data.MOBO.map(r => renderRow(r.key, r.value)).join('');

        // Network
        const netEl = document.getElementById('sysinfo-network');
        if (data.NET.length) netEl.innerHTML = data.NET.map(r => renderRow(r.key, r.value, r.key === 'External IP')).join('');

        loading.classList.add('hidden');
        grid.classList.remove('hidden');
        sysInfoLoaded = true;
    }, 4000);
}

// Refresh button
document.getElementById('sysinfo-refresh')?.addEventListener('click', () => {
    sysInfoLoaded = false;
    loadFullSystemInfo();
});

// (Keyboard shortcuts are defined in the earlier Keyboard Shortcuts section)

// ──────────────────────────────────────────────
// NetTriage — Network Diagnostics
// ──────────────────────────────────────────────

const netdiagBtn = document.getElementById('run-netdiag-btn');
const netdiagProgress = document.getElementById('netdiag-progress');
const netdiagStatusText = document.getElementById('netdiag-status-text');
const netdiagResults = document.getElementById('netdiag-results');

function renderNetdiagItem(gridId, label, value, status, extraClass) {
    const grid = document.getElementById(gridId);
    const item = document.createElement('div');
    item.className = `netdiag-item ${status}`;
    const valClass = extraClass || (status === 'pass' ? 'pass' : status === 'fail' ? 'fail' : 'info');
    item.innerHTML = `<span class="netdiag-label">${escapeHtml(label)}</span><span class="netdiag-value ${valClass}">${escapeHtml(String(value))}</span>`;
    grid.appendChild(item);
}

function renderSpeedItem(gridId, label, speedMbps) {
    const grid = document.getElementById(gridId);
    const item = document.createElement('div');
    item.className = 'netdiag-item speed-item pass';
    item.innerHTML = `<span class="netdiag-label">${escapeHtml(label)}</span><span class="speed-result">${speedMbps}<span class="speed-unit">Mbps</span></span>`;
    grid.appendChild(item);
}

function latencyClass(ms) {
    if (ms < 0) return 'fail';
    if (ms <= 30) return 'latency-good';
    if (ms <= 100) return 'latency-ok';
    return 'latency-bad';
}

function latencyStatus(ms) {
    return ms < 0 ? 'fail' : 'pass';
}

async function runNetTriage() {
    netdiagBtn.disabled = true;
    netdiagBtn.textContent = 'Running...';
    netdiagProgress.classList.remove('hidden');
    netdiagResults.classList.add('hidden');

    // Clear previous results
    ['netdiag-env', 'netdiag-ping', 'netdiag-tcp', 'netdiag-dns', 'netdiag-http', 'netdiag-speed'].forEach(id => {
        document.getElementById(id).innerHTML = '';
    });

    const speedProgress = document.getElementById('speed-progress');
    const speedBar = document.getElementById('speed-bar');
    speedProgress.classList.add('hidden');
    speedBar.style.width = '0%';

    logToTerminal('NetTriage: Starting network diagnostics...', 'INFO');

    try {
        // 1. Environment + External IP
        netdiagStatusText.textContent = 'Checking network environment...';
        await window.invokeX.runPowerShell(`
      $ErrorActionPreference='SilentlyContinue'
      $cfg=Get-NetIPConfiguration|Where-Object{$_.NetAdapter.Status -eq 'Up' -and $_.IPv4DefaultGateway -and $_.IPv4Address}|Sort-Object @{Expression={if($_.InterfaceAlias -match 'Wi-?Fi|Ethernet'){0}else{1}}}|Select-Object -First 1
      if($cfg){
        Write-Host "NETDIAG_GW|$($cfg.IPv4DefaultGateway.NextHop)"
        Write-Host "NETDIAG_IP|$($cfg.IPv4Address.IPAddress)"
        Write-Host "NETDIAG_IFACE|$($cfg.InterfaceAlias)"
      }else{
        Write-Host "NETDIAG_GW|NONE"; Write-Host "NETDIAG_IP|NONE"; Write-Host "NETDIAG_IFACE|NONE"
      }
      $dns=if($cfg){$cfg.DnsServer.ServerAddresses|Where-Object{$_ -match '^[0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+$'}|Select-Object -First 1}else{$null}
      if($dns){Write-Host "NETDIAG_DNS|$dns"}else{Write-Host "NETDIAG_DNS|NONE"}
      try{$ext=(Invoke-RestMethod -Uri 'https://api.ipify.org' -TimeoutSec 5);Write-Host "NETDIAG_EXTIP|$ext"}catch{Write-Host "NETDIAG_EXTIP|FAILED"}
    `);

        // 2. Latency (ping with ms) — PS 5.1 compatible
        netdiagStatusText.textContent = 'Measuring latency...';
        await window.invokeX.runPowerShell(`
      $ErrorActionPreference='SilentlyContinue'
      $cfg=Get-NetIPConfiguration|Where-Object{$_.NetAdapter.Status -eq 'Up' -and $_.IPv4DefaultGateway}|Select-Object -First 1
      $gw=if($cfg){$cfg.IPv4DefaultGateway.NextHop}else{$null}
      function Get-PingMs($target){
        if(-not $target){return -1}
        $results=Test-Connection -ComputerName $target -Count 3 -EA SilentlyContinue
        if($results){
          $avg=[math]::Round(($results|Measure-Object -Property ResponseTime -Average).Average,1)
          return $avg
        }
        return -1
      }
      Write-Host "NETDIAG_LAT_GW|$(Get-PingMs $gw)"
      Write-Host "NETDIAG_LAT_CF|$(Get-PingMs '1.1.1.1')"
      Write-Host "NETDIAG_LAT_GOOGLE|$(Get-PingMs '8.8.8.8')"
    `);

        // 3. TCP 443
        netdiagStatusText.textContent = 'Testing TCP 443 connectivity...';
        await window.invokeX.runPowerShell(`
      $ErrorActionPreference='SilentlyContinue'
      Write-Host "NETDIAG_TCP_1111|$([bool](Test-NetConnection -ComputerName '1.1.1.1' -Port 443 -InformationLevel Quiet))"
      Write-Host "NETDIAG_TCP_8888|$([bool](Test-NetConnection -ComputerName '8.8.8.8' -Port 443 -InformationLevel Quiet))"
    `);

        // 4. DNS Resolution
        netdiagStatusText.textContent = 'Testing DNS resolution...';
        await window.invokeX.runPowerShell(`
      $ErrorActionPreference='SilentlyContinue'
      $count=0
      @('openai.com','bbc.co.uk','cloudflare.com','microsoft.com')|ForEach-Object{
        $ok=$false;try{Resolve-DnsName $_ -Type A -EA Stop|Out-Null;$ok=$true;$count++}catch{}
        Write-Host "NETDIAG_DNS_$($_.Replace('.','_'))|$ok"
      }
      Write-Host "NETDIAG_DNS_COUNT|$count"
    `);

        // 5. HTTP/S Requests
        netdiagStatusText.textContent = 'Testing HTTP connectivity...';
        await window.invokeX.runPowerShell(`
      $ErrorActionPreference='SilentlyContinue'
      $count=0
      @('https://www.google.com','https://openai.com','https://www.bbc.co.uk','https://cloudflare.com')|ForEach-Object{
        $ok=$false;try{Invoke-WebRequest -Uri $_ -Method Head -TimeoutSec 10 -UseBasicParsing -EA Stop|Out-Null;$ok=$true;$count++}catch{}
        $name=([uri]$_).Host.Replace('.','_').Replace('www_','')
        Write-Host "NETDIAG_HTTP_$name|$ok"
      }
      Write-Host "NETDIAG_HTTP_COUNT|$count"
    `);

        // 6. Speed Test (download) — uses WebClient for real throughput
        netdiagStatusText.textContent = 'Running speed test (download)...';
        speedProgress.classList.remove('hidden');
        speedBar.style.width = '30%';
        await window.invokeX.runPowerShell(`
      $ErrorActionPreference='SilentlyContinue'
      [Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12
      $wc=New-Object System.Net.WebClient
      $wc.Headers.Add('User-Agent','InvokeX/2.0')
      $url='https://speed.cloudflare.com/__down?bytes=25000000'
      $sw=[System.Diagnostics.Stopwatch]::StartNew()
      try{
        $data=$wc.DownloadData($url)
        $sw.Stop()
        $bytes=$data.Length
        $secs=$sw.Elapsed.TotalSeconds
        if($secs -gt 0 -and $bytes -gt 0){
          $mbps=[math]::Round(($bytes * 8 / $secs / 1000000),2)
          Write-Host "NETDIAG_DL_MBPS|$mbps"
          Write-Host "NETDIAG_DL_SECS|$([math]::Round($secs,2))"
        }else{
          Write-Host "NETDIAG_DL_MBPS|0"
          Write-Host "NETDIAG_DL_SECS|0"
        }
      }catch{
        Write-Host "NETDIAG_DL_MBPS|0"
        Write-Host "NETDIAG_DL_SECS|0"
      }finally{
        $wc.Dispose()
      }
    `);
        speedBar.style.width = '60%';

        // 7. Speed Test (upload) — uses WebClient for real throughput
        netdiagStatusText.textContent = 'Running speed test (upload)...';
        await window.invokeX.runPowerShell(`
      $ErrorActionPreference='SilentlyContinue'
      [Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12
      $wc=New-Object System.Net.WebClient
      $wc.Headers.Add('User-Agent','InvokeX/2.0')
      $data=[byte[]]::new(10000000)
      (New-Object Random).NextBytes($data)
      $sw=[System.Diagnostics.Stopwatch]::StartNew()
      try{
        $wc.UploadData('https://speed.cloudflare.com/__up',$data)|Out-Null
        $sw.Stop()
        $secs=$sw.Elapsed.TotalSeconds
        if($secs -gt 0){
          $mbps=[math]::Round(($data.Length * 8 / $secs / 1000000),2)
          Write-Host "NETDIAG_UL_MBPS|$mbps"
        }else{
          Write-Host "NETDIAG_UL_MBPS|0"
        }
      }catch{
        Write-Host "NETDIAG_UL_MBPS|0"
      }finally{
        $wc.Dispose()
      }
    `);
        speedBar.style.width = '100%';

    } catch (err) {
        logToTerminal(`NetTriage error: ${err.message}`, 'ERROR');
    }

    // Parse results from terminal output
    setTimeout(() => {
        const nd = {};
        terminalEl.querySelectorAll('.log-message').forEach(el => {
            const t = el.textContent;
            if (t.startsWith('NETDIAG_')) {
                const [key, val] = t.split('|');
                nd[key] = val;
            }
        });

        const toBool = v => v === 'True';

        // Environment
        renderNetdiagItem('netdiag-env', 'Interface', nd.NETDIAG_IFACE || 'Unknown', 'pass');
        renderNetdiagItem('netdiag-env', 'Local IP', nd.NETDIAG_IP || 'None', nd.NETDIAG_IP !== 'NONE' ? 'pass' : 'fail');
        renderNetdiagItem('netdiag-env', 'External IP', nd.NETDIAG_EXTIP || 'Failed', nd.NETDIAG_EXTIP && nd.NETDIAG_EXTIP !== 'FAILED' ? 'pass' : 'fail');
        renderNetdiagItem('netdiag-env', 'Gateway', nd.NETDIAG_GW || 'None', nd.NETDIAG_GW !== 'NONE' ? 'pass' : 'fail');
        renderNetdiagItem('netdiag-env', 'DNS Server', nd.NETDIAG_DNS || 'None', nd.NETDIAG_DNS !== 'NONE' ? 'pass' : 'fail');

        // Latency
        const latGw = parseFloat(nd.NETDIAG_LAT_GW) || -1;
        const latCf = parseFloat(nd.NETDIAG_LAT_CF) || -1;
        const latGg = parseFloat(nd.NETDIAG_LAT_GOOGLE) || -1;
        renderNetdiagItem('netdiag-ping', 'Gateway', latGw >= 0 ? `${latGw} ms` : 'TIMEOUT', latencyStatus(latGw), latencyClass(latGw));
        renderNetdiagItem('netdiag-ping', '1.1.1.1 (Cloudflare)', latCf >= 0 ? `${latCf} ms` : 'TIMEOUT', latencyStatus(latCf), latencyClass(latCf));
        renderNetdiagItem('netdiag-ping', '8.8.8.8 (Google)', latGg >= 0 ? `${latGg} ms` : 'TIMEOUT', latencyStatus(latGg), latencyClass(latGg));

        // TCP
        renderNetdiagItem('netdiag-tcp', '1.1.1.1:443', toBool(nd.NETDIAG_TCP_1111) ? 'PASS' : 'FAIL', toBool(nd.NETDIAG_TCP_1111) ? 'pass' : 'fail');
        renderNetdiagItem('netdiag-tcp', '8.8.8.8:443', toBool(nd.NETDIAG_TCP_8888) ? 'PASS' : 'FAIL', toBool(nd.NETDIAG_TCP_8888) ? 'pass' : 'fail');

        // DNS
        ['openai_com', 'bbc_co_uk', 'cloudflare_com', 'microsoft_com'].forEach(d => {
            const label = d.replace(/_/g, '.');
            const key = `NETDIAG_DNS_${d}`;
            renderNetdiagItem('netdiag-dns', label, toBool(nd[key]) ? 'PASS' : 'FAIL', toBool(nd[key]) ? 'pass' : 'fail');
        });

        // HTTP
        ['google_com', 'openai_com', 'bbc_co_uk', 'cloudflare_com'].forEach(d => {
            const label = d.replace(/_/g, '.');
            const key = `NETDIAG_HTTP_${d}`;
            renderNetdiagItem('netdiag-http', label, toBool(nd[key]) ? 'PASS' : 'FAIL', toBool(nd[key]) ? 'pass' : 'fail');
        });

        // Speed Test
        const dlMbps = parseFloat(nd.NETDIAG_DL_MBPS) || 0;
        const ulMbps = parseFloat(nd.NETDIAG_UL_MBPS) || 0;
        if (dlMbps > 0) renderSpeedItem('netdiag-speed', '↓ Download', dlMbps.toFixed(2));
        else renderNetdiagItem('netdiag-speed', '↓ Download', 'Failed', 'fail');
        if (ulMbps > 0) renderSpeedItem('netdiag-speed', '↑ Upload', ulMbps.toFixed(2));
        else renderNetdiagItem('netdiag-speed', '↑ Upload', 'Failed', 'fail');

        speedProgress.classList.add('hidden');

        // Diagnosis
        const dnsCount = parseInt(nd.NETDIAG_DNS_COUNT) || 0;
        const httpCount = parseInt(nd.NETDIAG_HTTP_COUNT) || 0;
        const tcpOk = toBool(nd.NETDIAG_TCP_1111) || toBool(nd.NETDIAG_TCP_8888);
        const pingGw = latGw >= 0;
        const noGw = nd.NETDIAG_GW === 'NONE';
        const allPingFail = latGw < 0 && latCf < 0 && latGg < 0;

        let diagnosis, severity;
        if (noGw) {
            diagnosis = '⚠️ No IPv4 default gateway detected. Check adapter, VPN, or route configuration.';
            severity = 'error';
        } else if (!tcpOk && dnsCount < 2 && httpCount < 2) {
            if (!pingGw) {
                diagnosis = '❌ Likely LOCAL/ROUTER or ISP outage — cannot reach gateway, TCP/DNS/HTTP all failing.';
                severity = 'error';
            } else {
                diagnosis = '⚠️ Likely ISP/UPSTREAM outage — gateway responds but internet checks failing.';
                severity = 'warn';
            }
        } else if (dnsCount < 2 && tcpOk) {
            diagnosis = '⚠️ DNS issue — internet reachable (TCP works) but name resolution failing. Try changing DNS servers.';
            severity = 'warn';
        } else if (httpCount < 2 && tcpOk && dnsCount >= 2) {
            diagnosis = '⚠️ Web/TLS/Proxy issue — internet + DNS mostly OK, but HTTPS checks failing.';
            severity = 'warn';
        } else if (allPingFail && tcpOk) {
            diagnosis = 'ℹ️ Connectivity OK but ICMP (ping) is blocked. Ignore ping failures.';
            severity = 'ok';
        } else {
            diagnosis = `✅ All checks passed! Download: ${dlMbps.toFixed(1)} Mbps | Upload: ${ulMbps.toFixed(1)} Mbps`;
            severity = 'ok';
        }

        const diagEl = document.getElementById('netdiag-diagnosis');
        diagEl.className = `netdiag-diagnosis ${severity}`;
        diagEl.textContent = diagnosis;

        netdiagResults.classList.remove('hidden');
        netdiagProgress.classList.add('hidden');
        netdiagBtn.disabled = false;
        netdiagBtn.textContent = '▶ Run Again';

        logToTerminal(`NetTriage: ${diagnosis}`, severity === 'ok' ? 'SUCCESS' : 'WARNING');
        showToast('Network diagnostics complete', severity === 'ok' ? 'success' : 'warning');
    }, 1500);
}

netdiagBtn.addEventListener('click', runNetTriage);

// ──────────────────────────────────────────────
// Section 19: Network Tools Page Handlers
// ──────────────────────────────────────────────
// Quick-action tools show results in a popup for easy reading.
// Ping and Tracert are long-running so they output to the terminal.

/**
 * Helper: Run a PowerShell command and show results in the popup.
 * Captures all output lines and presents them in the results modal.
 */
async function runAndShowPopup(title, command) {
    capturedOutput = [];
    isCapturingOutput = true;
    await window.invokeX.runPowerShell(command);
    isCapturingOutput = false;
    if (capturedOutput.length > 0) {
        showResultsPopup(title, capturedOutput);
    }
}

document.getElementById('ping-run-btn').addEventListener('click', async () => {
    const addr = document.getElementById('ping-address').value.trim() || '8.8.8.8';
    const count = parseInt(document.getElementById('ping-count').value) || 0;
    const doLog = document.getElementById('ping-log').checked;
    const safe = addr.replace(/[^a-zA-Z0-9.-]/g, '');
    const pingCmd = count > 0 ? `ping ${safe} -n ${count}` : `ping ${safe} -t`;
    logToTerminal(`Running: ${pingCmd}`, 'INFO');
    const cmd = doLog
        ? `Write-Host 'Pinging ${safe}...';$out=cmd /c '${pingCmd}';$out|ForEach-Object{Write-Host $_};$out|Out-File "$env:USERPROFILE\\Desktop\\ping_${safe.replace(/\./g, '_')}.log" -Encoding UTF8;Write-Host '';Write-Host 'Log saved to Desktop.'`
        : `Write-Host 'Pinging ${safe}...';cmd /c '${pingCmd}'|ForEach-Object{Write-Host $_}`;
    await runAndShowPopup(`Ping — ${safe}`, cmd);
});

document.getElementById('tracert-run-btn').addEventListener('click', async () => {
    const addr = document.getElementById('tracert-address').value.trim() || '8.8.8.8';
    const doLog = document.getElementById('tracert-log').checked;
    const safe = addr.replace(/[^a-zA-Z0-9.-]/g, '');
    logToTerminal(`Running: tracert ${safe}`, 'INFO');
    const cmd = doLog
        ? `Write-Host 'Tracing route to ${safe}...';$out=cmd /c 'tracert ${safe}';$out|ForEach-Object{Write-Host $_};$out|Out-File "$env:USERPROFILE\\Desktop\\tracert_${safe.replace(/\./g, '_')}.log" -Encoding UTF8;Write-Host '';Write-Host 'Log saved to Desktop.'`
        : `Write-Host 'Tracing route to ${safe}...';cmd /c 'tracert ${safe}'|ForEach-Object{Write-Host $_}`;
    await runAndShowPopup(`Traceroute — ${safe}`, cmd);
});

document.getElementById('nettools-flushdns').addEventListener('click', async () => {
    logToTerminal('Flushing DNS cache...', 'INFO');
    await runAndShowPopup('Flush DNS', 'ipconfig /flushdns');
});

document.getElementById('nettools-ipconfig').addEventListener('click', async () => {
    logToTerminal('Running ipconfig...', 'INFO');
    await runAndShowPopup('IPConfig', 'ipconfig');
});

document.getElementById('nettools-ipconfigall').addEventListener('click', async () => {
    logToTerminal('Running ipconfig /all...', 'INFO');
    await runAndShowPopup('IPConfig /all', 'ipconfig /all');
});

document.getElementById('nettools-netinfo').addEventListener('click', async () => {
    logToTerminal('Gathering network info...', 'INFO');
    await runAndShowPopup('Network Info', `Get-NetAdapter|Where-Object{$_.Status -eq 'Up'}|ForEach-Object{$ip=Get-NetIPAddress -InterfaceIndex $_.ifIndex -AddressFamily IPv4 -EA SilentlyContinue;$dns=Get-DnsClientServerAddress -InterfaceIndex $_.ifIndex -AddressFamily IPv4 -EA SilentlyContinue;Write-Host "Adapter: $($_.Name) [$($_.LinkSpeed)]";Write-Host "  IP: $($ip.IPAddress)";Write-Host "  DNS: $($dns.ServerAddresses -join ', ')";Write-Host "  MAC: $($_.MacAddress)";Write-Host ''}`);
});

// ──────────────────────────────────────────────
// Initialization
// ──────────────────────────────────────────────

async function initialize() {
    logToTerminal('InvokeX v2.0 starting...', 'INFO');

    const isAdmin = await window.invokeX.checkAdmin();
    const adminStatus = document.getElementById('admin-status');
    const statusDot = adminStatus.querySelector('.status-dot');
    const statusText = adminStatus.querySelector('.status-text');

    if (isAdmin) {
        statusDot.className = 'status-dot admin';
        statusText.textContent = 'Administrator';
        logToTerminal('Running as: Administrator', 'SUCCESS');
    } else {
        statusDot.className = 'status-dot no-admin';
        statusText.textContent = 'Standard User';
        logToTerminal('Running as: Standard User', 'WARNING');
        const banner = document.getElementById('admin-banner');
        banner.classList.remove('hidden');
        document.getElementById('restart-admin-btn').addEventListener('click', () => window.invokeX.restartAsAdmin());
        document.getElementById('dismiss-admin-btn').addEventListener('click', () => banner.classList.add('hidden'));
        setTimeout(() => banner.classList.add('hidden'), 10000);
    }

    const winVer = await window.invokeX.getWindowsVersion();
    document.getElementById('windows-version').textContent = winVer;
    document.getElementById('tweaks-subtitle').textContent = `Customize Windows settings and behavior • ${winVer}`;

    APPS.forEach(renderAppCard);
    TWEAKS.forEach(renderTweakCard);
    // loadSystemInfo removed — info now on the System page

    logToTerminal('Ready. Press Ctrl+K to search.', 'SUCCESS');
    showToast('InvokeX v2.0 ready', 'info');
}

initialize();
