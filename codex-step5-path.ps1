#Requires -Version 5.1
<#
.SYNOPSIS
    5단계 - 앱이 기대하는 실제 경로를 앱 데이터에서 직접 추출

.DESCRIPTION
    4단계에서 구성요소를 "가장 최근 폴더"로 복사했으나 증상이 그대로입니다.
    설정 파일에서 참조를 찾지 못해 활성 폴더를 추정했기 때문에,
    앱이 실제로 바라보는 폴더가 다른 곳일 수 있습니다.

    이 스크립트는 앱 데이터 전체에서 'code-mode-host' 문자열을 찾아
    그 줄에 적힌 경로를 뽑아내고, 그 경로가 실제로 존재하는지 대조합니다.
    추정이 아니라 앱이 남긴 기록으로 기대 경로를 확정합니다.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\codex-step5-path.ps1
#>

[CmdletBinding()]
param()

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

Clear-Host
Write-Host ''
Write-Host '  5단계 - 앱이 기대하는 경로 추출' -ForegroundColor White
Write-Host '  -------------------------------' -ForegroundColor DarkGray

$Roots = @(
    (Join-PathSafe $env:LOCALAPPDATA 'OpenAI'),
    (Join-PathSafe $env:APPDATA      'OpenAI'),
    (Join-PathSafe $env:LOCALAPPDATA 'ChatGPT'),
    (Join-PathSafe $env:APPDATA      'ChatGPT'),
    (Join-PathSafe $env:USERPROFILE  '.codex')
) | Where-Object { $_ -and (Test-Path $_) } | Select-Object -Unique

if ($Roots.Count -eq 0) { Write-Bad '앱 데이터 폴더를 찾지 못했습니다.'; return }

# ------------------------------- 1. 현재 bin 폴더 상태 (복사 후)
Write-Section '1. 현재 bin 폴더 상태'

$BinRoot = Join-PathSafe $env:LOCALAPPDATA 'OpenAI\Codex\bin'
if ($BinRoot -and (Test-Path $BinRoot)) {
    Write-Info "bin: $BinRoot"
    foreach ($d in (Get-ChildItem $BinRoot -Directory -EA SilentlyContinue | Sort-Object LastWriteTime -Descending)) {
        $files = Get-ChildItem $d.FullName -File -Force -EA SilentlyContinue
        Write-Host ''
        Write-Host "   $($d.Name)   ($($d.LastWriteTime.ToString('yyyy-MM-dd HH:mm')))" -ForegroundColor White
        if (-not $files) { Write-Bad '     (비어 있음)' }
        foreach ($f in ($files | Sort-Object Name)) {
            Write-Host ("     {0,-44} {1,14:N0}" -f $f.Name, $f.Length) -ForegroundColor DarkGray
        }
    }
} else {
    Write-Warn 'bin 폴더를 찾지 못했습니다.'
}

# --------------------- 2. 'code-mode-host' 문자열이 든 파일 찾기
Write-Section '2. 앱 데이터에서 code-mode-host 기록 검색'

$Interesting = @()   # 설정/매니페스트/로그 계열 (경로가 적혀 있을 가능성 높음)
$Sessions    = 0     # 대화 세션 기록 (노이즈)

foreach ($r in $Roots) {
    $files = Get-ChildItem -Path $r -File -Recurse -Force -EA SilentlyContinue |
             Where-Object { $_.Length -lt 20MB }
    foreach ($f in $files) {
        try {
            if (-not (Select-String -Path $f.FullName -Pattern 'code-mode-host' -SimpleMatch -Quiet -EA SilentlyContinue)) { continue }
        } catch { continue }

        # 세션 대화 기록은 노이즈이므로 분리한다
        if ($f.Extension -match '(?i)^\.(jsonl|ndjson)$' -or $f.DirectoryName -match '(?i)session|rollout|history') {
            $Sessions++
        } else {
            $Interesting += $f
        }
    }
}

Write-Info "대화 세션 기록에서 발견: $Sessions 개 파일 (참고용, 무시)"
Write-Info "설정/로그 계열에서 발견: $($Interesting.Count) 개 파일"

# ------------------------------------ 3. 기록에서 경로 추출 및 대조
Write-Section '3. 기록된 경로 추출 및 실재 여부 대조'

# Windows 절대 경로 패턴 (JSON 안의 이스케이프된 역슬래시도 처리)
$pathRegex = '[A-Za-z]:\\\\?(?:[^"\r\n<>|*?]+?\\\\?)*codex-code-mode-host\.exe'
$foundPaths = @{}

$scanList = @()
$scanList += $Interesting
# 설정 계열에서 아무것도 못 찾으면 세션 기록에서도 경로를 찾아본다
if ($Interesting.Count -eq 0) {
    Write-Info '설정 계열이 없어 세션 기록에서도 경로를 찾아봅니다...'
    foreach ($r in $Roots) {
        $scanList += Get-ChildItem -Path $r -File -Recurse -Force -EA SilentlyContinue |
                     Where-Object { $_.Length -lt 20MB -and $_.Extension -match '(?i)^\.(jsonl|ndjson|log|txt|json)$' } |
                     Sort-Object LastWriteTime -Descending | Select-Object -First 40
    }
}

foreach ($f in ($scanList | Select-Object -First 120)) {
    try {
        $hits = Select-String -Path $f.FullName -Pattern $pathRegex -AllMatches -EA SilentlyContinue |
                Select-Object -First 5
        foreach ($h in $hits) {
            foreach ($m in $h.Matches) {
                $raw  = $m.Value
                $norm = $raw -replace '\\\\', '\'
                if (-not $foundPaths.ContainsKey($norm)) {
                    $foundPaths[$norm] = $f.Name
                }
            }
        }
    } catch { }
}

if ($foundPaths.Count -eq 0) {
    Write-Warn '기록에서 전체 경로를 추출하지 못했습니다.'
    Write-Info '=> 앱이 경로를 로그에 남기지 않는 방식입니다. 재설치로 진행하세요.'

    if ($Interesting.Count -gt 0) {
        Write-Host ''
        Write-Info '참고 - code-mode-host 가 언급된 설정/로그 파일:'
        foreach ($f in ($Interesting | Select-Object -First 10)) {
            Write-Host "     $($f.FullName)" -ForegroundColor DarkGray
        }
    }
} else {
    Write-Info "추출된 경로 $($foundPaths.Count) 개"
    Write-Host ''
    $missingPaths = @()
    foreach ($k in ($foundPaths.Keys | Sort-Object)) {
        $exists = Test-Path $k
        if ($exists) {
            Write-Ok "존재함 : $k"
        } else {
            Write-Bad "없음   : $k"
            Write-Info "         (기록 출처: $($foundPaths[$k]))"
            $missingPaths += $k
        }
    }

    if ($missingPaths.Count -gt 0) {
        Write-Host ''
        Write-Bad '앱이 기대하는 경로에 파일이 없습니다. <== 확정된 원인'
        Write-Host ''
        Write-Info '이 경로들로 파일을 복사하면 해결될 수 있습니다.'
        Write-Host ''
        Write-Host '  --- 복사 명령 (그대로 붙여넣기) ---' -ForegroundColor White
        $src = Get-ChildItem -Path $BinRoot -Filter 'codex-code-mode-host.exe' -Recurse -File -Force -EA SilentlyContinue |
               Sort-Object Length -Descending | Select-Object -First 1
        foreach ($mp in $missingPaths) {
            $destDir = Split-Path $mp -Parent
            Write-Host ("  New-Item -ItemType Directory -Force -Path `"$destDir`" | Out-Null") -ForegroundColor Cyan
            if ($src) {
                Write-Host ("  Copy-Item `"$($src.FullName)`" `"$mp`" -Force") -ForegroundColor Cyan
            }
        }
        Write-Host '  ----------------------------------' -ForegroundColor White
    } else {
        Write-Ok '기록된 경로에 파일이 모두 존재합니다.'
        Write-Info '=> 경로 문제가 아닙니다. 버전 불일치일 가능성이 높으니 재설치하세요.'
    }
}

# ----------------------------------------------- 4. 매니페스트 확인
Write-Section '4. 매니페스트 / 버전 파일'

$manifests = @()
foreach ($r in $Roots) {
    $manifests += Get-ChildItem -Path $r -File -Recurse -Force -EA SilentlyContinue |
                  Where-Object { $_.Name -match '(?i)(manifest|version|install|update|release)' -and $_.Length -lt 1MB }
}
$manifests = $manifests | Select-Object -First 15

if (-not $manifests) {
    Write-Info '매니페스트로 보이는 파일이 없습니다.'
} else {
    foreach ($m in $manifests) {
        Write-Host ''
        Write-Host "   $($m.FullName)" -ForegroundColor Yellow
        Write-Info ("     수정 $($m.LastWriteTime) / {0:N0} bytes" -f $m.Length)
        try {
            $txt = Get-Content $m.FullName -Raw -EA SilentlyContinue
            if ($txt -and $txt.Length -lt 4000) {
                Write-Host ($txt.Trim()) -ForegroundColor DarkGray
            } elseif ($txt) {
                Write-Host ($txt.Substring(0, 1200).Trim() + ' ...') -ForegroundColor DarkGray
            }
        } catch { }
    }
}

Write-Section '정리'
Write-Host '  위 2~4번 내용을 캡처해 공유해 주세요.' -ForegroundColor White
Write-Host '  경로가 확정되면 재설치 없이 해결할 수 있습니다.' -ForegroundColor Gray
Write-Host ''
