# LatencyTest.ps1 - Parameterized network latency tester for InvokeX
# Accepts parameters (no interactive prompts) for Electron IPC execution.
# Outputs structured LATTEST_* lines for renderer parsing.

param(
    [Parameter(Mandatory=$true)][string]$Destination,
    [int]$Port = 443,
    [int]$PingCount = 20,
    [int]$TcpCount = 20,
    [int]$TimeoutMs = 3000,
    [switch]$DoTracert
)

$ErrorActionPreference = "SilentlyContinue"

# --- Auto-detect gateway ---
$cfg = Get-NetIPConfiguration |
    Where-Object { $_.NetAdapter.Status -eq "Up" -and $_.IPv4DefaultGateway -and $_.IPv4Address } |
    Sort-Object @{
        Expression = {
            $name = $_.InterfaceAlias
            if ($name -match "Wi-?Fi|Ethernet") { 0 } else { 1 }
        }
    }
$first = $cfg | Select-Object -First 1
$gateway = if ($first) { $first.IPv4DefaultGateway.NextHop } else { "192.168.1.1" }
$knownGood = "1.1.1.1"

Write-Host "LATTEST_CFG|Destination|${Destination}:${Port}"
Write-Host "LATTEST_CFG|Gateway|$gateway"
Write-Host "LATTEST_CFG|Known Good|$knownGood"
Write-Host "LATTEST_CFG|Ping Count|$PingCount"
Write-Host "LATTEST_CFG|TCP Samples|$TcpCount"

# --- Ping Stats Function ---
function Get-PingStats {
    param([string]$Target, [int]$Count)
    $r = Test-Connection -TargetName $Target -Count $Count -ErrorAction SilentlyContinue
    if (-not $r) {
        return [pscustomobject]@{
            Lost = $Count; LossPct = 100; MinMs = $null; AvgMs = $null; MaxMs = $null; Note = "No replies"
        }
    }
    $mo = $r | Measure-Object ResponseTime -Minimum -Average -Maximum
    $recv = $r.Count
    $lost = $Count - $recv
    $loss = [math]::Round(($lost / $Count) * 100, 2)
    [pscustomobject]@{
        Lost = $lost; LossPct = $loss
        MinMs = [int]$mo.Minimum; AvgMs = [math]::Round($mo.Average, 1); MaxMs = [int]$mo.Maximum
        Note = ""
    }
}

# --- TCP Latency Function ---
function Get-TcpLatency {
    param([string]$HostOrIp, [int]$Port, [int]$Count, [int]$TmoMs)
    $results = 1..$Count | ForEach-Object {
        $sw = [Diagnostics.Stopwatch]::StartNew()
        $client = New-Object Net.Sockets.TcpClient
        try {
            $iar = $client.BeginConnect($HostOrIp, $Port, $null, $null)
            if (-not $iar.AsyncWaitHandle.WaitOne($TmoMs, $false)) { throw "timeout" }
            $client.EndConnect($iar)
            $sw.Stop()
            $sw.ElapsedMilliseconds
        } catch { $null } finally { $client.Close() }
    }
    $ok = $results | Where-Object { $_ -ne $null }
    if (-not $ok) {
        return [pscustomobject]@{
            Success = 0; MinMs = $null; AvgMs = $null; P95Ms = $null; MaxMs = $null; JitterAbs = $null
            Note = "All failed/timed out"
        }
    }
    $s = $ok | Sort-Object
    $avg = ($ok | Measure-Object -Average).Average
    $p95 = $s[[math]::Max(0, [math]::Floor($s.Count * 0.95) - 1)]
    $jitter = [math]::Round(($ok | ForEach-Object { [math]::Abs($_ - $avg) } | Measure-Object -Average).Average, 1)
    [pscustomobject]@{
        Success = $ok.Count
        MinMs = [int]$s[0]; AvgMs = [math]::Round($avg, 1); P95Ms = [int]$p95; MaxMs = [int]$s[-1]
        JitterAbs = $jitter; Note = ""
    }
}

# --- Run Tests ---

# Gateway Ping
$gwPing = Get-PingStats -Target $gateway -Count $PingCount
Write-Host "LATTEST_GWPING|Loss|$($gwPing.LossPct)%"
Write-Host "LATTEST_GWPING|Min|$(if($gwPing.MinMs -ne $null){"$($gwPing.MinMs) ms"}else{'N/A'})"
Write-Host "LATTEST_GWPING|Avg|$(if($gwPing.AvgMs -ne $null){"$($gwPing.AvgMs) ms"}else{'N/A'})"
Write-Host "LATTEST_GWPING|Max|$(if($gwPing.MaxMs -ne $null){"$($gwPing.MaxMs) ms"}else{'N/A'})"

# Known-Good Ping
$kgPing = Get-PingStats -Target $knownGood -Count $PingCount
Write-Host "LATTEST_KGPING|Loss|$($kgPing.LossPct)%"
Write-Host "LATTEST_KGPING|Min|$(if($kgPing.MinMs -ne $null){"$($kgPing.MinMs) ms"}else{'N/A'})"
Write-Host "LATTEST_KGPING|Avg|$(if($kgPing.AvgMs -ne $null){"$($kgPing.AvgMs) ms"}else{'N/A'})"
Write-Host "LATTEST_KGPING|Max|$(if($kgPing.MaxMs -ne $null){"$($kgPing.MaxMs) ms"}else{'N/A'})"

# TCP Latency
$tcp = Get-TcpLatency -HostOrIp $Destination -Port $Port -Count $TcpCount -TmoMs $TimeoutMs
Write-Host "LATTEST_TCP|Success|$($tcp.Success)/$TcpCount"
Write-Host "LATTEST_TCP|Min|$(if($tcp.MinMs -ne $null){"$($tcp.MinMs) ms"}else{'N/A'})"
Write-Host "LATTEST_TCP|Avg|$(if($tcp.AvgMs -ne $null){"$($tcp.AvgMs) ms"}else{'N/A'})"
Write-Host "LATTEST_TCP|P95|$(if($tcp.P95Ms -ne $null){"$($tcp.P95Ms) ms"}else{'N/A'})"
Write-Host "LATTEST_TCP|Max|$(if($tcp.MaxMs -ne $null){"$($tcp.MaxMs) ms"}else{'N/A'})"
Write-Host "LATTEST_TCP|Jitter|$(if($tcp.JitterAbs -ne $null){"$($tcp.JitterAbs) ms"}else{'N/A'})"

# Tracert (optional)
if ($DoTracert) {
    $trLines = cmd /c "tracert -d $Destination"
    $trOutput = ($trLines -join "`n")
    Write-Host "LATTEST_TRACERT|$trOutput"
}

# --- Diagnosis ---
if ($gwPing.LossPct -ge 5 -or ($gwPing.AvgMs -ne $null -and $gwPing.AvgMs -ge 30)) {
    $diag = "Likely local LAN/Wi-Fi/router issue (gateway ping is poor)"
    $sev = "warn"
}
elseif ($kgPing.LossPct -ge 5 -or ($kgPing.AvgMs -ne $null -and $kgPing.AvgMs -ge 150)) {
    $diag = "Likely ISP/upstream issue (known-good ping is poor)"
    $sev = "warn"
}
elseif ($tcp.Success -lt [math]::Max(1, [math]::Floor($TcpCount * 0.8))) {
    $diag = "Likely firewall/routing issue to destination (many TCP failures)"
    $sev = "warn"
}
elseif ($tcp.P95Ms -ne $null -and ($tcp.P95Ms -ge 500 -or $tcp.AvgMs -ge 200)) {
    $diag = "High latency/jitter on destination path (congestion or bufferbloat)"
    $sev = "warn"
}
else {
    $diag = "Looks generally OK"
    $sev = "ok"
}

Write-Host "LATTEST_DIAG|$sev|$diag"