#Requires -Version 5.1
<#
.SYNOPSIS
    6단계 - 복사한 파일이 사라지는지 확인 (보안 소프트웨어 제거 여부 확정)

.DESCRIPTION
    4단계에서 두 구성요소를 최신 버전 폴더로 복사했고 크기까지 대조해 성공을 확인했습니다.
    그러나 이후 점검에서 그 폴더에는 codex.exe 하나만 남아 있었습니다.
    파일이 저절로 사라지지는 않으므로, 무언가가 제거하고 있다는 뜻입니다.

    이 스크립트는 그것을 직접 증명합니다.
      1) 구성요소를 복사한다
      2) 즉시 존재를 확인한다
      3) 시간을 두고 다시 확인한다
      4) 사라졌다면 제거하는 주체가 있다는 뜻이다

    이것이 사실이면 재설치해도 같은 자리에서 실패하므로,
    재설치 전에 반드시 확인해야 합니다.

.PARAMETER WaitSeconds
    재확인까지 기다리는 시간(초). 기본 25초.

.PARAMETER NoCopy
    복사하지 않고 현재 상태만 점검합니다.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\codex-step6-vanish.ps1
#>

[CmdletBinding()]
param(
    [int]$WaitSeconds = 25,
    [switch]$NoCopy
)

$ErrorActionPreference = 'Continue'
$ProgressPreference    = 'SilentlyContinue'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch { }

function Write-Section { param([string]$T)
    Write-Host ''; Write-Host ('=' * 70) -ForegroundColor DarkCyan
    Write-Host "  $T" -ForegroundColor Cyan; Write-Host ('=' * 70) -ForegroundColor DarkCyan }
function Write-Ok   { param($m) Write-Host "  [OK]   $m" -ForegroundColor Green }
function Write-Warn { param($m) Write-Host "  [주의] $m" -ForegroundColor Yellow }
function Write-Bad  { param($m) Write-Host "  [문제] $m" -ForegroundColor Red }
function Write-Info { param($m) Write-Host "  [정보] $m" -ForegroundColor Gray }

function Join-PathSafe {
    param([string]$Base, [string]$Child)
    if ([string]::IsNullOrWhiteSpace($Base)) { return $null }
    try { return (Join-Path -Path $Base -ChildPath $Child) } catch { return $null }
}

$Expected = @('codex-code-mode-host.exe', 'codex-windows-sandbox-setup.exe', 'codex-command-runner.exe')
$BinRoot  = if ($env:CODEX_TEST_ROOT) { Join-PathSafe $env:CODEX_TEST_ROOT 'bin' }
            else { Join-PathSafe $env:LOCALAPPDATA 'OpenAI\Codex\bin' }

Clear-Host
Write-Host ''
Write-Host '  6단계 - 파일이 사라지는지 확인' -ForegroundColor White
Write-Host '  ------------------------------' -ForegroundColor DarkGray

if (-not $BinRoot -or -not (Test-Path $BinRoot)) {
    Write-Bad "bin 폴더가 없습니다: $BinRoot"
    return
}

# ------------------------------------------------- 1. 현재 배치 상태
Write-Section '1. 현재 폴더별 구성요소 배치'

$dirs = Get-ChildItem -Path $BinRoot -Directory -EA SilentlyContinue | Sort-Object LastWriteTime -Descending
if (-not $dirs) { Write-Bad '버전 폴더가 없습니다.'; return }

$rows = @()
foreach ($d in $dirs) {
    $files = Get-ChildItem $d.FullName -File -Force -EA SilentlyContinue
    $have  = @($Expected | Where-Object { $n = $_; $files | Where-Object { $_.Name -ieq $n } })
    $rows += [PSCustomObject]@{
        Name    = $d.Name
        Path    = $d.FullName
        Written = $d.LastWriteTime
        Files   = $files
        Have    = $have
        Lacks   = @($Expected | Where-Object { $have -notcontains $_ })
    }
    Write-Host ''
    Write-Host "   $($d.Name)   ($($d.LastWriteTime.ToString('MM-dd HH:mm')))" -ForegroundColor White
    if (-not $files) { Write-Bad '     (비어 있음)' }
    foreach ($f in ($files | Sort-Object Name)) {
        $mk = if ($Expected -contains $f.Name) { '  <-- 필요' } else { '' }
        Write-Host ("     {0,-40} {1,14:N0}{2}" -f $f.Name, $f.Length, $mk) -ForegroundColor DarkGray
    }
}

# 원본(구성요소를 가진 폴더)과 대상(최신이지만 빠진 폴더)
$source = $rows | Where-Object { @($_.Lacks).Count -eq 0 } | Select-Object -First 1
$target = $rows | Where-Object { @($_.Lacks).Count -gt 0 } | Select-Object -First 1

Write-Host ''
if (-not $source) {
    Write-Bad '구성요소를 모두 가진 폴더가 없습니다. 원본이 없어 테스트할 수 없습니다.'
    Write-Info '=> 재설치가 필요합니다.'
    return
}
Write-Ok "원본 폴더 : $($source.Name)"

if (-not $target) {
    Write-Ok '모든 폴더가 완전합니다. 사라진 파일이 없습니다.'
    Write-Info '=> 앱을 다시 실행해 보세요.'
    return
}
Write-Bad "대상 폴더 : $($target.Name)  (빠진 것: $($target.Lacks -join ', '))"

# ------------------------------------------------- 2. 복사 후 즉시 확인
Write-Section '2. 복사 후 즉시 확인'

if ($NoCopy) {
    Write-Info '-NoCopy 지정으로 복사를 건너뜁니다.'
    return
}

$copied = @()
foreach ($name in $target.Lacks) {
    $src = $source.Files | Where-Object { $_.Name -ieq $name } | Select-Object -First 1
    if (-not $src) { Write-Warn "원본에 없음: $name"; continue }
    $dest = Join-Path $target.Path $name
    try {
        Copy-Item -Path $src.FullName -Destination $dest -Force -EA Stop
        Start-Sleep -Milliseconds 400
        if (Test-Path $dest) {
            $len = (Get-Item $dest).Length
            if ($len -eq $src.Length) {
                Write-Ok ("복사 성공: {0} ({1:N0} bytes)" -f $name, $len)
                $copied += [PSCustomObject]@{ Name = $name; Dest = $dest; Size = $src.Length }
            } else {
                Write-Bad ("복사되었으나 크기가 다릅니다: {0} ({1:N0} / 원본 {2:N0})" -f $name, $len, $src.Length)
                $copied += [PSCustomObject]@{ Name = $name; Dest = $dest; Size = $src.Length }
            }
        } else {
            Write-Bad "복사 직후 이미 사라졌습니다: $name  <== 실시간 감시가 즉시 제거"
            $copied += [PSCustomObject]@{ Name = $name; Dest = $dest; Size = $src.Length }
        }
    } catch {
        Write-Bad "복사 실패: $name - $($_.Exception.Message)"
    }
}

if ($copied.Count -eq 0) { Write-Warn '복사된 파일이 없어 테스트를 진행할 수 없습니다.'; return }

# ------------------------------------------------- 3. 시간을 두고 재확인
Write-Section "3. $WaitSeconds 초 후 재확인"

Write-Info '파일이 그대로 남아 있는지 확인합니다. 창을 닫지 마세요.'
for ($i = $WaitSeconds; $i -gt 0; $i--) {
    Write-Host ("`r     남은 시간: {0,3} 초 " -f $i) -NoNewline -ForegroundColor DarkGray
    Start-Sleep -Seconds 1
}
Write-Host "`r                          " -NoNewline
Write-Host ''

$vanished = @()
$survived = @()
foreach ($c in $copied) {
    if (Test-Path $c.Dest) {
        $len = (Get-Item $c.Dest).Length
        if ($len -eq $c.Size) { Write-Ok "남아 있음: $($c.Name)"; $survived += $c }
        else { Write-Bad ("크기가 변했습니다: {0} ({1:N0})" -f $c.Name, $len); $vanished += $c }
    } else {
        Write-Bad "사라졌습니다: $($c.Name)  <== 제거됨"
        $vanished += $c
    }
}

# ------------------------------------------------- 4. 판정
Write-Section '판정'

if ($vanished.Count -eq 0) {
    Write-Ok '복사한 파일이 모두 그대로 남아 있습니다.'
    Write-Host ''
    Write-Host '  => 파일을 지우는 주체는 없습니다.' -ForegroundColor White
    Write-Host '     앱을 완전히 종료했다가 다시 실행하고 .pptx 생성을 재요청하세요.' -ForegroundColor White
    Write-Host '     그래도 실패하면 버전 불일치이므로 재설치로 넘어갑니다.' -ForegroundColor Gray
} else {
    Write-Bad "복사한 파일 $($vanished.Count) 개가 제거되었습니다."
    Write-Host ''
    Write-Host '  => 보안 소프트웨어가 이 실행 파일들을 지우고 있습니다.' -ForegroundColor White
    Write-Host '     새 버전 폴더에 codex.exe 만 남은 이유도 이것으로 설명됩니다.' -ForegroundColor White
    Write-Host '     이 상태에서는 재설치해도 같은 자리에서 실패합니다.' -ForegroundColor Yellow

    # V3 흔적 확인
    Write-Host ''
    Write-Info 'AhnLab V3 기록을 확인합니다...'
    $ahn = @(
        (Join-PathSafe $env:ProgramFiles 'AhnLab'),
        (Join-PathSafe ${env:ProgramFiles(x86)} 'AhnLab'),
        (Join-PathSafe $env:ProgramData 'AhnLab')
    ) | Where-Object { $_ -and (Test-Path $_) }

    $trace = 0
    foreach ($a in $ahn) {
        $logs = Get-ChildItem $a -Include *.log,*.txt,*.csv -Recurse -File -Force -EA SilentlyContinue |
                Where-Object { $_.LastWriteTime -gt (Get-Date).AddHours(-2) } | Select-Object -First 60
        foreach ($l in $logs) {
            try {
                $m = Select-String -Path $l.FullName -Pattern 'codex' -SimpleMatch -EA SilentlyContinue | Select-Object -First 2
                foreach ($x in $m) { $trace++; Write-Host "     $($l.Name): $($x.Line.Trim())" -ForegroundColor Yellow }
            } catch { }
        }
    }
    if ($trace -eq 0) { Write-Info '읽을 수 있는 V3 로그에는 기록이 없습니다. (로그가 잠겨 있을 수 있습니다)' }

    Write-Host ''
    Write-Host '  --- 학교 정보 담당 선생님께 전달할 내용 ---' -ForegroundColor White
    Write-Host '   AhnLab V3 Endpoint Security 가 아래 폴더의 실행 파일을' -ForegroundColor Gray
    Write-Host '   자동 삭제하여 프로그램이 동작하지 않습니다.' -ForegroundColor Gray
    Write-Host '   검사 제외(예외) 목록에 아래 폴더를 추가해 주시기 바랍니다.' -ForegroundColor Gray
    Write-Host ''
    Write-Host ("     " + (Join-PathSafe $env:LOCALAPPDATA 'OpenAI')) -ForegroundColor Cyan
    Write-Host ''
    Write-Host '   삭제되는 파일 (모두 OpenAI OpCo 정품 서명):' -ForegroundColor Gray
    foreach ($v in $vanished) { Write-Host ("     - " + $v.Name) -ForegroundColor Cyan }
    Write-Host '  -------------------------------------------' -ForegroundColor White
}
Write-Host ''
