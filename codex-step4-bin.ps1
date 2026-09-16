#Requires -Version 5.1
<#
.SYNOPSIS
    4단계 - 버전 폴더 불일치 확정 및 구성요소 배치 복구

.DESCRIPTION
    3단계에서 확인된 사실:
      - codex-code-mode-host.exe        : 디스크에 존재
      - codex-windows-sandbox-setup.exe : 디스크에 존재
      - 미완성 다운로드 없음
      - bin 버전 폴더가 여러 개

    두 파일이 모두 있는데 앱이 "찾을 수 없음"이라고 하므로,
    앱이 바라보는 버전 폴더에 파일이 없고 다른 폴더에 들어 있을 가능성이 높습니다.

    이 스크립트는 어느 폴더에 무엇이 있는지 표로 보여주고,
    -Repair 를 쓰면 부족한 구성요소를 활성 폴더로 복사합니다. (파일 삭제는 하지 않습니다)

.PARAMETER Repair
    구성요소가 빠진 활성 폴더로 파일을 복사합니다. 기존 파일은 덮어쓰지 않습니다.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\codex-step4-bin.ps1

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\codex-step4-bin.ps1 -Repair
#>

[CmdletBinding()]
param([switch]$Repair)

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

$Expected  = @('codex-code-mode-host.exe', 'codex-windows-sandbox-setup.exe')

# 평상시에는 표준 설치 경로를 사용한다.
# CODEX_TEST_ROOT 환경변수가 있으면 그 경로를 대신 검사한다 (검증용).
if ($env:CODEX_TEST_ROOT) { $CodexRoot = $env:CODEX_TEST_ROOT }
else { $CodexRoot = Join-PathSafe $env:LOCALAPPDATA 'OpenAI\Codex' }
$BinRoot = Join-PathSafe $CodexRoot 'bin'

Clear-Host
Write-Host ''
Write-Host '  4단계 - 버전 폴더 불일치 확정' -ForegroundColor White
Write-Host '  -----------------------------' -ForegroundColor DarkGray

if (-not $BinRoot -or -not (Test-Path $BinRoot)) {
    Write-Bad "bin 폴더가 없습니다: $BinRoot"
    Write-Info '재설치가 필요합니다.'
    return
}

# --------------------------------------- 1. 폴더별 구성요소 배치표
Write-Section '1. 버전 폴더별 구성요소 배치'

$dirs = Get-ChildItem -Path $BinRoot -Directory -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending

if (-not $dirs) {
    Write-Bad 'bin 폴더 안에 버전 폴더가 없습니다. 재설치가 필요합니다.'
    return
}

Write-Info "bin 폴더: $BinRoot"
Write-Info "버전 폴더 $($dirs.Count) 개 (최근 수정순)"
Write-Host ''

# 표 머리글
$h1 = 'host.exe'; $h2 = 'sandbox-setup.exe'
Write-Host ("   {0,-3} {1,-22} {2,-20} {3,-10} {4,-18}" -f '#', '폴더', '수정일', $h1, $h2) -ForegroundColor White
Write-Host ('   ' + ('-' * 76)) -ForegroundColor DarkGray

$table = @()
$idx = 0
foreach ($d in $dirs) {
    $idx++
    $files = Get-ChildItem -Path $d.FullName -File -Force -ErrorAction SilentlyContinue
    $hasHost = [bool]($files | Where-Object { $_.Name -ieq $Expected[0] })
    $hasSbx  = [bool]($files | Where-Object { $_.Name -ieq $Expected[1] })

    $row = [PSCustomObject]@{
        Index   = $idx
        Name    = $d.Name
        Path    = $d.FullName
        Written = $d.LastWriteTime
        FileCount = $files.Count
        HasHost = $hasHost
        HasSbx  = $hasSbx
    }
    $table += $row

    $m1 = if ($hasHost) { '  있음  ' } else { '  없음  ' }
    $m2 = if ($hasSbx)  { '  있음  ' } else { '  없음  ' }
    $color = if ($hasHost -and $hasSbx) { 'Green' } else { 'Red' }
    Write-Host ("   {0,-3} {1,-22} {2,-20} {3,-10} {4,-18}" -f `
        $idx, $d.Name, $d.LastWriteTime.ToString('yyyy-MM-dd HH:mm'), $m1, $m2) -ForegroundColor $color
}

Write-Host ''
$complete   = $table | Where-Object { $_.HasHost -and $_.HasSbx }
$incomplete = $table | Where-Object { -not ($_.HasHost -and $_.HasSbx) }

$completeCount   = @($complete).Count
$incompleteCount = @($incomplete).Count
if ($completeCount   -gt 0) { Write-Ok   "두 구성요소를 모두 가진 폴더: $completeCount 개" }
if ($incompleteCount -gt 0) { Write-Warn "구성요소가 빠진 폴더: $incompleteCount 개" }

if ($incompleteCount -eq 0) {
    Write-Ok '모든 버전 폴더가 완전합니다. 배치 문제는 아닙니다.'
}

# ------------------------------------ 2. 앱이 실제로 쓰는 폴더 찾기
Write-Section '2. 앱이 바라보는 버전 폴더 추적'

$active = $null
$cfgHits = @()

if ($CodexRoot -and (Test-Path $CodexRoot)) {
    $cfgFiles = Get-ChildItem -Path $CodexRoot -File -Recurse -Force -ErrorAction SilentlyContinue |
                Where-Object {
                    $_.Length -lt 2MB -and
                    $_.FullName -notmatch '\\bin\\' -and
                    $_.Extension -match '(?i)^\.(json|toml|ini|cfg|txt|yaml|yml|lock)$'
                } | Select-Object -First 300

    Write-Info "설정 파일 $($cfgFiles.Count) 개에서 폴더 이름을 검색합니다..."

    foreach ($c in $cfgFiles) {
        foreach ($row in $table) {
            try {
                if (Select-String -Path $c.FullName -Pattern $row.Name -SimpleMatch -Quiet -ErrorAction SilentlyContinue) {
                    $cfgHits += [PSCustomObject]@{ File = $c.Name; Folder = $row.Name; Row = $row }
                }
            } catch { }
        }
    }
}

if ($cfgHits.Count -gt 0) {
    Write-Host ''
    Write-Info '설정 파일이 참조하는 폴더:'
    foreach ($x in ($cfgHits | Select-Object -First 10)) {
        Write-Host "     $($x.File)  ->  $($x.Folder)" -ForegroundColor Yellow
    }
    $active = ($cfgHits | Select-Object -First 1).Row
    Write-Ok "활성 폴더로 판단: $($active.Name)"
} else {
    Write-Warn '설정 파일에서 참조를 찾지 못했습니다.'
    $active = $table | Select-Object -First 1
    Write-Info "가장 최근 폴더를 활성으로 간주합니다: $($active.Name)"
}

Write-Host ''
if ($active.HasHost -and $active.HasSbx) {
    Write-Ok '활성 폴더에 두 구성요소가 모두 있습니다.'
    Write-Info '=> 버전 폴더 배치 문제는 아닙니다. 재설치가 필요합니다.'
} else {
    Write-Bad '활성 폴더에 구성요소가 빠져 있습니다. <== 이것이 원인입니다.'
    if (-not $active.HasHost) { Write-Bad "   없음: $($Expected[0])" }
    if (-not $active.HasSbx)  { Write-Bad "   없음: $($Expected[1])" }
}

# ---------------------------------------------- 3. 복구 (파일 복사)
Write-Section '3. 구성요소 배치 복구'

$needed = @()
foreach ($e in $Expected) {
    $have = if ($e -ieq $Expected[0]) { $active.HasHost } else { $active.HasSbx }
    if (-not $have) { $needed += $e }
}

if ($needed.Count -eq 0) {
    Write-Ok '복사할 구성요소가 없습니다.'
} else {
    Write-Info "활성 폴더에 채워야 할 구성요소: $($needed -join ', ')"

    # 다른 폴더 전체에서 원본 찾기
    $plan = @()
    foreach ($e in $needed) {
        $src = Get-ChildItem -Path $BinRoot -Filter $e -Recurse -File -Force -ErrorAction SilentlyContinue |
               Sort-Object LastWriteTime -Descending | Select-Object -First 1
        if ($src) {
            $sigOk = $false
            try {
                $sg = Get-AuthenticodeSignature -FilePath $src.FullName -ErrorAction Stop
                $sigOk = ($sg.Status -eq 'Valid')
            } catch { }
            Write-Info "  원본 발견: $e"
            Write-Info ("     $($src.FullName)")
            Write-Info ("     크기 {0:N0} bytes / 서명 {1}" -f $src.Length, $(if ($sigOk) { '정상' } else { '확인 불가' }))
            if (-not $sigOk) {
                Write-Warn '     서명을 확인하지 못했습니다. (카탈로그 서명이면 정상일 수 있습니다)'
                Write-Info  '     원본이 앱 자신의 설치 폴더 안에 있으므로 복사는 진행합니다.'
            }
            $plan += [PSCustomObject]@{ Name = $e; Source = $src; SigOk = $sigOk }
        } else {
            Write-Bad "  원본을 찾지 못했습니다: $e"
        }
    }

    if ($plan.Count -eq 0) {
        Write-Warn '복사 가능한 원본이 없습니다. 재설치가 필요합니다.'
    } elseif (-not $Repair) {
        Write-Host ''
        Write-Info "-Repair 옵션을 붙이면 위 $($plan.Count) 개를 활성 폴더로 복사합니다."
        Write-Info '기존 파일은 덮어쓰지 않으며, 파일을 삭제하지도 않습니다.'
    } else {
        Write-Host ''
        foreach ($item in $plan) {
            $dest = Join-Path $active.Path $item.Name
            if (Test-Path $dest) { Write-Info "이미 존재하므로 건너뜁니다: $($item.Name)"; continue }
            try {
                Copy-Item -Path $item.Source.FullName -Destination $dest -ErrorAction Stop
                $ok = Test-Path $dest
                if ($ok) {
                    $dl = (Get-Item $dest).Length
                    if ($dl -eq $item.Source.Length) { Write-Ok "복사 완료: $($item.Name) ($('{0:N0}' -f $dl) bytes)" }
                    else { Write-Bad "복사했으나 크기가 다릅니다: $($item.Name)" }
                }
            } catch {
                Write-Bad "복사 실패: $($item.Name) - $($_.Exception.Message)"
                Write-Info '  관리자 권한으로 다시 실행해 보세요.'
            }
        }
    }
}

# ------------------------------------------------------- 4. 결론
Write-Section '결론'

if ($active.HasHost -and $active.HasSbx) {
    Write-Host '  활성 폴더는 완전합니다. 배치 문제가 아닙니다.' -ForegroundColor White
    Write-Host ''
    Write-Host '  => 재설치를 진행하세요:' -ForegroundColor White
    Write-Host '     1) codex-step3-logs.ps1 을 -Clean 으로 실행 (앱 완전 종료)' -ForegroundColor Gray
    Write-Host '     2) 설정 > 앱 에서 ChatGPT 제거' -ForegroundColor Gray
    Write-Host ("     3) 폴더 삭제: " + (Join-PathSafe $env:LOCALAPPDATA 'OpenAI')) -ForegroundColor Gray
    Write-Host '     4) 공식 페이지에서 다시 받아 관리자 권한으로 설치' -ForegroundColor Gray
} elseif ($Repair) {
    Write-Host '  구성요소를 활성 폴더로 복사했습니다.' -ForegroundColor White
    Write-Host ''
    Write-Host '  => 이제 앱을 완전히 종료했다가 다시 실행하고,' -ForegroundColor White
    Write-Host '     대화창에 ".pptx 파일로 만들어줘" 를 재요청하세요.' -ForegroundColor White
    Write-Host '     실패하면 위 재설치 절차로 넘어가세요.' -ForegroundColor Gray
} else {
    Write-Host '  => 아래를 실행해 복구를 시도하세요:' -ForegroundColor White
    Write-Host ("     powershell -ExecutionPolicy Bypass -File `"$PSCommandPath`" -Repair") -ForegroundColor Cyan
}
Write-Host ''
