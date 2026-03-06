# NetTriage.ps1 - LAN vs Internet (ASCII only, popup summary)
# Works on Windows PowerShell 5.1+

$ErrorActionPreference = "SilentlyContinue"

function Show-Popup($Title, $Message) {
  Add-Type -AssemblyName System.Windows.Forms | Out-Null
  [System.Windows.Forms.MessageBox]::Show(
    $Message, $Title,
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Information
  ) | Out-Null
}

function Get-ActiveIPv4Gateway {
  $cfg = Get-NetIPConfiguration |
    Where-Object { $_.NetAdapter.Status -eq "Up" -and $_.IPv4DefaultGateway -and $_.IPv4Address } |
    Sort-Object @{
      Expression = {
        $name = $_.InterfaceAlias
        if ($name -match "Wi-?Fi|Ethernet") { 0 } else { 1 }
      }
    }

  $first = $cfg | Select-Object -First 1
  if ($first) { return $first.IPv4DefaultGateway.NextHop }
  return $null
}

function Get-ActiveIPv4Dns {
  $cfg = Get-NetIPConfiguration |
    Where-Object { $_.NetAdapter.Status -eq "Up" -and $_.IPv4Address } |
    Sort-Object @{
      Expression = {
        $name = $_.InterfaceAlias
        if ($name -match "Wi-?Fi|Ethernet") { 0 } else { 1 }
      }
    } |
    Select-Object -First 1

  if ($cfg -and $cfg.DnsServer.ServerAddresses) {
    return ($cfg.DnsServer.ServerAddresses |
      Where-Object { $_ -match '^\d+\.\d+\.\d+\.\d+$' } |
      Select-Object -First 1)
  }
  return $null
}

function Test-PingOnce($Host) {
  if (-not $Host) { return $false }
  return [bool](Test-Connection -TargetName $Host -Count 1 -Quiet)
}

function Test-Tcp443($Host) {
  if (-not $Host) { return $false }
  return [bool](Test-NetConnection -ComputerName $Host -Port 443 -InformationLevel Quiet)
}

function Test-DnsNameOk($Name) {
  try { Resolve-DnsName $Name -Type A -ErrorAction Stop | Out-Null; return $true }
  catch { return $false }
}

function Test-HttpHeadOk($Url) {
  try { Invoke-WebRequest -Uri $Url -Method Head -TimeoutSec 10 -UseBasicParsing -ErrorAction Stop | Out-Null; return $true }
  catch { return $false }
}

# Gather environment
$gateway = Get-ActiveIPv4Gateway
$dns1    = Get-ActiveIPv4Dns

# Tests
$pingGw = Test-PingOnce $gateway
$ping11 = Test-PingOnce "1.1.1.1"
$ping88 = Test-PingOnce "8.8.8.8"

$tcp11  = Test-Tcp443 "1.1.1.1"
$tcp88  = Test-Tcp443 "8.8.8.8"

$dnsOkCount = 0
foreach ($n in @("openai.com","bbc.co.uk","cloudflare.com","microsoft.com")) {
  if (Test-DnsNameOk $n) { $dnsOkCount++ }
}

$httpOkCount = 0
foreach ($u in @("https://www.google.com","https://openai.com","https://www.bbc.co.uk","https://cloudflare.com")) {
  if (Test-HttpHeadOk $u) { $httpOkCount++ }
}

$tcpOkCount = @($tcp11,$tcp88 | Where-Object { $_ }).Count
$icmpAllFail = (-not $pingGw) -and (-not $ping11) -and (-not $ping88)
$icmpProbablyBlocked = $icmpAllFail -and ($tcpOkCount -ge 1)

# Diagnosis
if (-not $gateway) {
  $diagnosis = "No IPv4 default gateway detected (adapter/VPN/route issue)."
}
elseif (-not $tcp11 -and -not $tcp88 -and $dnsOkCount -lt 2 -and $httpOkCount -lt 2) {
  if (-not $pingGw) {
    $diagnosis = "Likely LOCAL/ROUTER or ISP outage (cannot confirm gateway via ping; TCP/DNS/HTTP also failing)."
  } else {
    $diagnosis = "Likely ISP/UPSTREAM outage (gateway responds but internet checks failing)."
  }
}
elseif ($dnsOkCount -lt 2 -and ($tcpOkCount -ge 1)) {
  $diagnosis = "DNS issue: internet reachable (TCP works) but name resolution failing."
}
elseif ($httpOkCount -lt 2 -and ($tcpOkCount -ge 1) -and ($dnsOkCount -ge 2)) {
  $diagnosis = "Web/TLS/Proxy issue: internet + DNS mostly OK, but HTTPS checks failing."
}
elseif ($icmpProbablyBlocked) {
  $diagnosis = "Connectivity looks OK but ICMP (ping) is blocked, so ignore ping results."
}
else {
  $diagnosis = "Looks OK right now. If issues are intermittent, run again during the problem window."
}

# Popup message (CRLF newlines)
$msg  = "Net Triage Summary`r`n`r`n"
$msg += "Gateway: " + ($(if ($gateway) { $gateway } else { "(none)" })) + "`r`n"
$msg += "DNS:     " + ($(if ($dns1)    { $dns1 }    else { "(none)" })) + "`r`n`r`n"
$msg += "Ping (ICMP): GW=" + $pingGw + "  1.1.1.1=" + $ping11 + "  8.8.8.8=" + $ping88 + "`r`n"
$msg += "TCP 443:     1.1.1.1=" + $tcp11 + "  8.8.8.8=" + $tcp88 + "`r`n`r`n"
$msg += "DNS resolves OK:  " + $dnsOkCount + " / 4`r`n"
$msg += "HTTP checks OK:   " + $httpOkCount + " / 4`r`n`r`n"
$msg += "Diagnosis:`r`n" + $diagnosis + "`r`n"

Show-Popup "Internet Check Result" $msg
Write-Host $msg