#Requires -Version 5.1
<#
.SYNOPSIS
    Codex / ChatGPT 데스크톱 앱의 "codex-code-mode-host.exe 누락" 오류 진단 및 복구 도구

.DESCRIPTION
    파일 생성(.pptx, .xlsx 등)과 코드 실행에 쓰이는 보조 실행 프로세스가
    사라졌을 때, 가장 흔한 원인 4가지를 순서대로 점검하고 복구합니다.

      1. 실행 파일이 실제로 존재하는지 (설치 불완전 / 업데이트 중단)
      2. Windows Defender가 격리(검역)했는지  -> 복원
      3. 인터넷 다운로드 차단 플래그(Zone.Identifier)가 걸렸는지 -> 해제
      4. 설치 경로에 한글/특수문자가 있는지, 제3자 백신이 있는지

.PARAMETER Fix
    실제 복구 작업까지 수행합니다. 생략하면 진단만 하고 아무것도 바꾸지 않습니다.

.PARAMETER SkipExclusion
    -Fix 를 쓰되, 백신 예외(제외 경로) 등록만은 건너뜁니다.

.EXAMPLE
    # 1단계: 진단만 (아무것도 바꾸지 않음)
    powershell -ExecutionPolicy Bypass -File .\fix-codex-host.ps1

.EXAMPLE
    # 2단계: 복구 실행 (관리자 권한 PowerShell 권장)
    powershell -ExecutionPolicy Bypass -File .\fix-codex-host.ps1 -Fix
#>

[CmdletBinding()]
param(
    [switch]$Fix,
    [switch]$SkipExclusion
)

$ErrorActionPreference = 'Continue'
$ProgressPreference    = 'SilentlyContinue'

# 콘솔 한글 깨짐 방지
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch { }

$TargetExe = 'codex-code-mode-host.exe'
$Findings  = [System.Collections.Generic.List[string]]::new()
$Actions   = [System.Collections.Generic.List[string]]::new()

function Write-Section {
    param([string]$Title)
    Write-Host ''
    Write-Host ('=' * 66) -ForegroundColor DarkCyan
    Write-Host "  $Title" -ForegroundColor Cyan
    Write-Host ('=' * 66) -ForegroundColor DarkCyan
}

function Write-Ok   { param($m) Write-Host "  [OK]   $m" -ForegroundColor Green }
function Write-Warn { param($m) Write-Host "  [주의] $m" -ForegroundColor Yellow }
function Write-Bad  { param($m) Write-Host "  [문제] $m" -ForegroundColor Red }
function Write-Info { param($m) Write-Host "  [정보] $m" -ForegroundColor Gray }

function Join-PathSafe {
    # 환경변수가 비어 있으면 Join-Path 가 오류를 내므로 null 을 반환한다
    param([string]$Base, [string]$Child)
    if ([string]::IsNullOrWhiteSpace($Base)) { return $null }
    try { return (Join-Path -Path $Base -ChildPath $Child) } catch { return $null }
}

function Test-Admin {
    try {
        $id = [Security.Principal.WindowsIdentity]::GetCurrent()
        return ([Security.Principal.WindowsPrincipal]$id).IsInRole(
            [Security.Principal.WindowsBuiltInRole]::Administrator)
    } catch { return $false }
}

# ---------------------------------------------------------------- 0. 시작
Clear-Host
Write-Host ''
Write-Host '  Codex 실행 도구(codex-code-mode-host.exe) 복구 진단' -ForegroundColor White
Write-Host '  ------------------------------------------------------' -ForegroundColor DarkGray

$IsAdmin = Test-Admin
if ($Fix -and -not $IsAdmin) {
    Write-Warn '관리자 권한이 아닙니다. 격리 복원 / 백신 예외 등록이 실패할 수 있습니다.'
    Write-Info 'PowerShell 아이콘 우클릭 > "관리자 권한으로 실행" 후 다시 돌려주세요.'
}
if (-not $Fix) {
    Write-Info '진단 모드입니다. 시스템을 변경하지 않습니다. 복구하려면 -Fix 를 붙이세요.'
}

$osName = 'Unknown'
try { $osName = (Get-CimInstance Win32_OperatingSystem -ErrorAction Stop).Caption } catch { }
Write-Info ("OS        : " + $osName)
Write-Info ("PowerShell: " + $PSVersionTable.PSVersion)
Write-Info ("관리자     : " + $(if ($IsAdmin) { '예' } else { '아니오' }))

# ------------------------------------------------- 1. 앱 설치 폴더 찾기
Write-Section '1. 앱 설치 폴더 탐색'

$SearchRoots = @(
    (Join-PathSafe $env:LOCALAPPDATA 'Programs'),
    $env:LOCALAPPDATA,
    $env:APPDATA,
    $env:ProgramFiles,
    ${env:ProgramFiles(x86)},
    $env:ProgramData
) | Where-Object { $_ -and (Test-Path $_) } | Select-Object -Unique

$AppRoots = @()
foreach ($root in $SearchRoots) {
    try {
        $hits = Get-ChildItem -Path $root -Directory -ErrorAction SilentlyContinue |
                Where-Object { $_.Name -match '(?i)codex|chatgpt|openai' }
        foreach ($h in $hits) { $AppRoots += $h.FullName }
    } catch { }
}
$AppRoots = $AppRoots | Select-Object -Unique

if ($AppRoots.Count -eq 0) {
    Write-Bad '설치 폴더를 찾지 못했습니다. 앱이 제거되었거나 비표준 경로에 있습니다.'
    $Findings.Add('앱 설치 폴더 자체가 발견되지 않음 -> 재설치 필요')
} else {
    foreach ($a in $AppRoots) { Write-Ok $a }
}

# --------------------------------------------- 2. 실행 파일 존재 확인
Write-Section "2. $TargetExe 존재 확인"

$ExeHits = @()
$ScanRoots = if ($AppRoots.Count -gt 0) { $AppRoots } else { $SearchRoots }
foreach ($root in $ScanRoots) {
    try {
        $found = Get-ChildItem -Path $root -Filter $TargetExe -Recurse -File -Force -ErrorAction SilentlyContinue
        foreach ($f in $found) { $ExeHits += $f }
    } catch { }
}
$ExeHits = $ExeHits | Sort-Object FullName -Unique

if ($ExeHits.Count -gt 0) {
    foreach ($e in $ExeHits) {
        Write-Ok "발견: $($e.FullName)"
        Write-Info ("  크기 : {0:N0} bytes / 수정일 {1}" -f $e.Length, $e.LastWriteTime)

        if ($e.Length -lt 1024) {
            Write-Bad '  파일 크기가 비정상적으로 작습니다. 다운로드가 잘린 것으로 보입니다.'
            $Findings.Add('실행 파일이 손상(0바이트에 가까움) -> 재설치 필요')
        }

        # 디지털 서명 확인
        try {
            $sig = Get-AuthenticodeSignature -FilePath $e.FullName -ErrorAction SilentlyContinue
            if ($sig.Status -eq 'Valid') {
                Write-Ok "  서명 : 정상 ($($sig.SignerCertificate.Subject -replace '^CN=([^,]+).*','$1'))"
            } else {
                Write-Warn "  서명 : $($sig.Status) - 위변조되었거나 서명이 없습니다."
            }
        } catch { }

        # 다운로드 차단 플래그
        $zone = Get-Item -Path $e.FullName -Stream Zone.Identifier -ErrorAction SilentlyContinue
        if ($zone) {
            Write-Bad '  차단 : "다른 컴퓨터에서 가져온 파일" 플래그가 걸려 실행이 막혀 있습니다.'
            $Findings.Add('Zone.Identifier 차단 플래그')
            if ($Fix) {
                Unblock-File -Path $e.FullName -ErrorAction SilentlyContinue
                Write-Ok '  -> 차단 해제 완료'
                $Actions.Add("차단 해제: $($e.FullName)")
            }
        } else {
            Write-Ok '  차단 : 없음'
        }
    }
} else {
    Write-Bad "$TargetExe 를 어디에서도 찾지 못했습니다. (이것이 오류의 직접 원인입니다)"
    $Findings.Add("$TargetExe 파일이 디스크에 없음")
}

# ------------------------------------- 3. Windows Defender 격리 확인
Write-Section '3. Windows Defender 격리(검역) 확인'

$Quarantined = @()
try {
    $detections = Get-MpThreatDetection -ErrorAction Stop
    foreach ($d in $detections) {
        $res = @($d.Resources) -join ' '
        if ($res -match '(?i)codex|chatgpt|openai') { $Quarantined += $d }
    }

    if ($Quarantined.Count -gt 0) {
        Write-Bad "Defender가 관련 파일을 격리했습니다. ($($Quarantined.Count)건) <- 가장 흔한 원인"
        $Findings.Add('Windows Defender가 실행 파일을 격리함')
        foreach ($q in $Quarantined) {
            Write-Info ("  탐지명: " + $q.ThreatID + " / 시각: " + $q.InitialDetectionTime)
            foreach ($r in @($q.Resources)) { Write-Info "  대상  : $r" }
        }
    } else {
        Write-Ok 'Defender 격리 이력에서 관련 항목이 발견되지 않았습니다.'
    }
} catch {
    Write-Warn 'Defender 상태를 조회할 수 없습니다 (비활성화되었거나 제3자 백신 사용 중).'
}

# MpCmdRun.exe 위치 확인 후 격리 목록 출력 / 복원
$MpCmd = $null
foreach ($c in @(
        (Join-PathSafe $env:ProgramFiles 'Windows Defender\MpCmdRun.exe'),
        (Join-PathSafe $env:ProgramData  'Microsoft\Windows Defender\Platform'))) {
    if ($c -and (Test-Path $c)) {
        if ((Get-Item $c).PSIsContainer) {
            $latest = Get-ChildItem $c -Directory -ErrorAction SilentlyContinue |
                      Sort-Object Name -Descending | Select-Object -First 1
            if ($latest) {
                $cand = Join-Path $latest.FullName 'MpCmdRun.exe'
                if (Test-Path $cand) { $MpCmd = $cand; break }
            }
        } else { $MpCmd = $c; break }
    }
}

if ($MpCmd) {
    Write-Info "MpCmdRun : $MpCmd"
    $list = & $MpCmd -Restore -ListAll 2>&1 | Out-String
    if ($list -match '(?i)codex|chatgpt|openai') {
        Write-Bad '격리함에 Codex 관련 항목이 남아 있습니다.'
        Write-Host $list -ForegroundColor DarkGray
        $Findings.Add('Defender 격리함에 복원 대기 항목 존재')

        if ($Fix) {
            if (-not $IsAdmin) {
                Write-Warn '복원에는 관리자 권한이 필요합니다. 건너뜁니다.'
            } else {
                # codex 관련 항목만 선별 복원 (전체 복원은 실제 악성코드까지 되살릴 수 있어 사용하지 않음)
                foreach ($line in ($list -split "`r?`n")) {
                    if ($line -match '(?i)(codex|chatgpt|openai)') {
                        $name = ($line -split ':',2)[-1].Trim()
                        if ($name) {
                            Write-Info "복원 시도: $name"
                            & $MpCmd -Restore -Name $name 2>&1 | Out-String | Write-Host -ForegroundColor DarkGray
                            $Actions.Add("Defender 격리 복원 시도: $name")
                        }
                    }
                }
                Write-Ok '격리 복원 명령을 실행했습니다.'
            }
        }
    } else {
        Write-Ok '격리함에 Codex 관련 항목이 없습니다.'
    }
}

# --------------------------------------------- 4. 제3자 백신 확인
Write-Section '4. 설치된 백신 제품 확인'

try {
    $av = Get-CimInstance -Namespace 'root/SecurityCenter2' -ClassName AntiVirusProduct -ErrorAction Stop
    foreach ($p in $av) {
        if ($p.displayName -match '(?i)defender') {
            Write-Ok "백신: $($p.displayName)"
        } else {
            Write-Warn "제3자 백신 감지: $($p.displayName)"
            Write-Info '  -> 이 백신의 "격리 보관함 / 차단 기록"도 직접 확인해 주세요.'
            Write-Info '     (V3, 알약, Avast, McAfee 등이 exe를 치우는 사례가 많습니다)'
            $Findings.Add("제3자 백신($($p.displayName))의 격리 여부 수동 확인 필요")
        }
    }
} catch {
    Write-Info '백신 목록을 조회하지 못했습니다.'
}

# ------------------------------- 5. 백신 예외 등록 (재격리 방지)
Write-Section '5. 백신 예외 등록 (재발 방지)'

if (-not $Fix) {
    Write-Info '-Fix 옵션과 함께 실행하면 앱 설치 폴더를 Defender 예외로 등록합니다.'
} elseif ($SkipExclusion) {
    Write-Info '-SkipExclusion 지정으로 건너뜁니다.'
} elseif (-not $IsAdmin) {
    Write-Warn '관리자 권한이 없어 예외 등록을 건너뜁니다.'
} elseif ($AppRoots.Count -eq 0) {
    Write-Warn '등록할 설치 폴더를 찾지 못해 건너뜁니다.'
} else {
    Write-Info '주의: 예외 등록은 해당 폴더의 실시간 검사를 끕니다.'
    Write-Info '      앱 설치 폴더에만 좁게 적용하며, 시스템 전체 보호는 유지됩니다.'
    foreach ($a in $AppRoots) {
        try {
            Add-MpPreference -ExclusionPath $a -ErrorAction Stop
            Write-Ok "예외 등록: $a"
            $Actions.Add("Defender 예외 등록: $a")
        } catch {
            Write-Warn "예외 등록 실패: $a ($($_.Exception.Message))"
        }
    }
    Write-Info '되돌리려면: Remove-MpPreference -ExclusionPath "<경로>"'
}

# ----------------------------------- 6. 경로 / 실행 환경 점검
Write-Section '6. 경로 및 실행 환경 점검'

foreach ($a in $AppRoots) {
    if ($a -match '[^\x00-\x7F]') {
        Write-Warn "설치 경로에 한글/비ASCII 문자가 있습니다: $a"
        Write-Info '  -> 일부 빌드에서 이 경우 보조 프로세스 실행이 실패합니다.'
        $Findings.Add('설치 경로에 한글 포함 -> 영문 경로로 재설치 권장')
    }
}

$procs = Get-Process -ErrorAction SilentlyContinue |
         Where-Object { $_.ProcessName -match '(?i)codex|chatgpt' }
if ($procs) {
    Write-Info '현재 실행 중인 관련 프로세스:'
    foreach ($p in $procs) { Write-Info "  $($p.ProcessName) (PID $($p.Id))" }
    Write-Warn '복구 후에는 앱을 완전히 종료했다가 다시 실행해야 적용됩니다.'
} else {
    Write-Ok '실행 중인 관련 프로세스가 없습니다.'
}

# 최근 앱 오류 이벤트
try {
    $evts = Get-WinEvent -FilterHashtable @{ LogName='Application'; Level=2; StartTime=(Get-Date).AddDays(-7) } `
            -MaxEvents 200 -ErrorAction SilentlyContinue |
            Where-Object { $_.Message -match '(?i)codex|chatgpt' } | Select-Object -First 5
    if ($evts) {
        Write-Warn '최근 7일간 관련 오류 이벤트:'
        foreach ($e in $evts) {
            Write-Info ("  " + $e.TimeCreated + " : " + ($e.Message -split "`n")[0])
        }
    }
} catch { }

# ------------------------------------------------------- 7. 요약
Write-Section '진단 요약'

if ($Findings.Count -eq 0) {
    Write-Ok '눈에 띄는 문제를 찾지 못했습니다.'
    Write-Info '앱을 완전히 종료(트레이 아이콘까지)한 뒤 재실행해 보세요.'
} else {
    Write-Host '  발견된 문제:' -ForegroundColor Yellow
    $i = 1
    foreach ($f in $Findings) { Write-Host "    $i) $f" -ForegroundColor Yellow; $i++ }
}

if ($Actions.Count -gt 0) {
    Write-Host ''
    Write-Host '  수행한 복구 작업:' -ForegroundColor Green
    foreach ($a in $Actions) { Write-Host "    - $a" -ForegroundColor Green }
}

Write-Host ''
Write-Host '  다음 단계' -ForegroundColor White
Write-Host '  ---------' -ForegroundColor DarkGray

if (-not $Fix) {
    Write-Host '   1. 관리자 권한 PowerShell에서 아래를 실행해 복구하세요:' -ForegroundColor White
    Write-Host "      powershell -ExecutionPolicy Bypass -File `"$PSCommandPath`" -Fix" -ForegroundColor Cyan
} elseif ($ExeHits.Count -eq 0) {
    Write-Host '   1. 실행 파일이 없으므로 재설치가 필요합니다.' -ForegroundColor White
    Write-Host '      - 앱을 완전히 제거 후, 설치했던 공식 경로에서 다시 내려받아' -ForegroundColor Gray
    Write-Host '        "관리자 권한으로 실행"하여 설치하세요.' -ForegroundColor Gray
    Write-Host '      - 설치 중에는 백신을 잠시 중지하면 재격리를 막을 수 있습니다.' -ForegroundColor Gray
    Write-Host '   2. 설치 후 이 스크립트를 -Fix 없이 다시 돌려 정상 여부를 확인하세요.' -ForegroundColor White
} else {
    Write-Host '   1. 앱을 완전히 종료하세요 (작업 표시줄 트레이 아이콘까지 우클릭 > 종료).' -ForegroundColor White
    Write-Host '   2. 앱을 다시 실행하세요.' -ForegroundColor White
    Write-Host '   3. 앱 설정에서 아래를 확인하세요:' -ForegroundColor White
    Write-Host '      - 파일 쓰기 / 로컬 실행 권한 허용' -ForegroundColor Gray
    Write-Host '      - 작업 폴더(워크스페이스) 지정 여부' -ForegroundColor Gray
    Write-Host '      - 웹 검색(네트워크 접근) 허용' -ForegroundColor Gray
    Write-Host '   4. 대화창에 "위 초안 그대로 .pptx 파일로 만들어줘" 라고 다시 요청하세요.' -ForegroundColor White
}
Write-Host ''
