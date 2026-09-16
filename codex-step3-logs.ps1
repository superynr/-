#Requires -Version 5.1
<#
.SYNOPSIS
    3단계 - 앱 로그에서 실제 오류 문구 추출 + bin 폴더 무결성 검사 + 좀비 프로세스 정리

.DESCRIPTION
    2단계에서 다음이 확인되었습니다.
      - codex-code-mode-host.exe 는 정상이며 서명도 유효함 (OpenAI OpCo)
      - 직접 실행 테스트 통과 -> 보안 소프트웨어 차단 아님
      - 좀비 프로세스(codex-computer-use-swift 등)가 남아 있었음

    따라서 남은 가능성은 두 가지입니다.
      (1) 좀비 프로세스 재발  -> -Clean 으로 즉시 정리
      (2) 앱 업데이트가 중간에 끊겨 bin 해시 폴더가 불완전함

    이 스크립트는 앱이 스스로 남긴 로그에서 실제 오류 문구를 찾아내
    추측이 아니라 근거로 원인을 확정합니다.

.PARAMETER Clean
    좀비 ChatGPT / codex 프로세스를 정리합니다.
    증상이 재발하면 이 옵션만 다시 실행하면 됩니다.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\codex-step3-logs.ps1

.EXAMPLE
    # 증상 재발 시 - 이것만 실행
    powershell -ExecutionPolicy Bypass -File .\codex-step3-logs.ps1 -Clean
#>

[CmdletBinding()]
param([switch]$Clean)

$ErrorActionPreference = 'Continue'
$ProgressPreference    = 'SilentlyContinue'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch { }

function Write-Section { param([string]$T)
    Write-Host ''; Write-Host ('=' * 66) -ForegroundColor DarkCyan
    Write-Host "  $T" -ForegroundColor Cyan; Write-Host ('=' * 66) -ForegroundColor DarkCyan }
function Write-Ok   { param($m) Write-Host "  [OK]   $m" -ForegroundColor Green }
function Write-Warn { param($m) Write-Host "  [주의] $m" -ForegroundColor Yellow }
function Write-Bad  { param($m) Write-Host "  [문제] $m" -ForegroundColor Red }
function Write-Info { param($m) Write-Host "  [정보] $m" -ForegroundColor Gray }

function Join-PathSafe {
    param([string]$Base, [string]$Child)
    if ([string]::IsNullOrWhiteSpace($Base)) { return $null }
    try { return (Join-Path -Path $Base -ChildPath $Child) } catch { return $null }
}

$Result = [System.Collections.Generic.List[string]]::new()

Clear-Host
Write-Host ''
Write-Host '  3단계 - 앱 로그 및 설치 무결성 검사' -ForegroundColor White
Write-Host '  ----------------------------------' -ForegroundColor DarkGray

# ------------------------------------- 1. 좀비 프로세스 즉시 확인
Write-Section '1. 좀비 프로세스 확인'

$stale = Get-Process -ErrorAction SilentlyContinue |
         Where-Object { $_.ProcessName -match '(?i)^(chatgpt|codex)' }

if (-not $stale) {
    Write-Ok '실행 중인 ChatGPT / codex 프로세스가 없습니다.'
} else {
    $groups = $stale | Group-Object ProcessName | Sort-Object Count -Descending
    foreach ($g in $groups) { Write-Info "$($g.Name) : $($g.Count) 개" }

    # 앱이 꺼져 있는데 codex 보조 프로세스만 남아 있으면 그것이 좀비다
    $hasUi     = $stale | Where-Object { $_.ProcessName -match '(?i)^chatgpt' }
    $hasHelper = $stale | Where-Object { $_.ProcessName -match '(?i)^codex' }

    if ($hasHelper -and -not $hasUi) {
        Write-Bad '앱 본체는 꺼져 있는데 codex 보조 프로세스가 남아 있습니다. <== 좀비입니다.'
        Write-Info '이 상태에서 앱을 켜면 또 "누락 오류"가 납니다.'
        $Result.Add('좀비 보조 프로세스 잔존 - 정리 필요')
    } else {
        Write-Info '앱이 실행 중인 것으로 보입니다. (정상일 수 있습니다)'
    }

    if ($Clean) {
        Write-Info '정리를 시작합니다...'
        foreach ($p in $stale) {
            try { $p.Kill(); Write-Info "  종료: $($p.ProcessName) (PID $($p.Id))" }
            catch { Write-Warn "  종료 실패: $($p.ProcessName) (PID $($p.Id))" }
        }
        Start-Sleep -Seconds 2
        $left = Get-Process -ErrorAction SilentlyContinue |
                Where-Object { $_.ProcessName -match '(?i)^(chatgpt|codex)' }
        if ($left) { Write-Warn "$($left.Count) 개가 남았습니다. 재부팅이 필요할 수 있습니다." }
        else { Write-Ok '정리 완료. 앱을 새로 실행하세요.' }
    } else {
        Write-Info '-Clean 옵션을 붙이면 모두 정리합니다.'
    }
}

# ------------------------------- 2. bin 해시 폴더 무결성 검사
Write-Section '2. 설치 구성요소 누락 검사'

# 앱이 "찾을 수 없다"고 보고한 실행 파일들
$Expected = @(
    'codex-code-mode-host.exe',
    'codex-windows-sandbox-setup.exe'
)

$OpenAIRoot = Join-PathSafe $env:LOCALAPPDATA 'OpenAI'
$BinRoot    = Join-PathSafe $env:LOCALAPPDATA 'OpenAI\Codex\bin'

# --- 2-1. 앱이 지목한 구성요소가 실제로 존재하는가 ---
if (-not $OpenAIRoot -or -not (Test-Path $OpenAIRoot)) {
    Write-Bad "설치 폴더를 찾지 못했습니다: $OpenAIRoot"
    $Result.Add('설치 폴더 없음 - 재설치 필요')
} else {
    Write-Info "설치 루트: $OpenAIRoot"
    $allExe = Get-ChildItem -Path $OpenAIRoot -Filter *.exe -Recurse -File -Force -ErrorAction SilentlyContinue
    Write-Info "설치된 실행 파일 총 $($allExe.Count) 개"
    Write-Host ''

    $missing = 0
    foreach ($name in $Expected) {
        $f = $allExe | Where-Object { $_.Name -ieq $name } | Select-Object -First 1
        if ($f) {
            Write-Ok "$name"
            Write-Info ("     경로: " + $f.FullName)
            Write-Info ("     크기: {0:N0} bytes / 수정 {1}" -f $f.Length, $f.LastWriteTime)
        } else {
            $missing++
            Write-Bad "$name  <== 실제로 없습니다"
            $Result.Add("$name 누락")
        }
    }

    if ($missing -gt 0) {
        Write-Host ''
        Write-Bad "앱이 보고한 누락이 사실로 확인되었습니다. ($missing 개)"
        Write-Info '설치 구성요소가 불완전합니다. 업데이트/설치가 중간에 끊긴 상태입니다.'
    }

    Write-Host ''
    Write-Info 'codex 관련 실행 파일 목록:'
    $codexExe = $allExe | Where-Object { $_.Name -match '(?i)codex' } | Sort-Object Name
    if (-not $codexExe) {
        Write-Bad '  codex 관련 실행 파일이 하나도 없습니다.'
    } else {
        foreach ($e in $codexExe) {
            Write-Host ("     {0,-42} {1,12:N0} bytes" -f $e.Name, $e.Length) -ForegroundColor DarkGray
        }
    }
}

# --- 2-2. bin 버전 폴더별 상세 ---
Write-Host ''
if (-not $BinRoot -or -not (Test-Path $BinRoot)) {
    Write-Warn "bin 폴더를 찾지 못했습니다: $BinRoot"
} else {
    Write-Info "bin 폴더: $BinRoot"
    $dirs = Get-ChildItem -Path $BinRoot -Directory -ErrorAction SilentlyContinue |
            Sort-Object LastWriteTime -Descending

    if (-not $dirs) {
        Write-Bad 'bin 폴더 안에 버전 폴더가 없습니다. 설치가 손상되었습니다.'
        $Result.Add('bin 폴더가 비어 있음 - 재설치 필요')
    } else {
        Write-Info "버전 폴더 $($dirs.Count) 개"
        $idx = 0
        foreach ($d in $dirs) {
            $idx++
            $files = Get-ChildItem -Path $d.FullName -File -Recurse -Force -ErrorAction SilentlyContinue
            $size  = ($files | Measure-Object -Property Length -Sum).Sum
            $tag   = if ($idx -eq 1) { ' (가장 최근)' } else { '' }

            Write-Host ''
            Write-Host "   [$idx] $($d.Name)$tag" -ForegroundColor White
            Write-Info ("     수정 : $($d.LastWriteTime)")
            Write-Info ("     내용 : $($files.Count) 개 파일 / {0:N1} MB" -f ($size / 1MB))

            foreach ($f in ($files | Sort-Object Name | Select-Object -First 25)) {
                $mark = if ($Expected -contains $f.Name) { '  <-- 필요 구성요소' } else { '' }
                Write-Host ("       {0,-42} {1,12:N0}{2}" -f $f.Name, $f.Length, $mark) -ForegroundColor DarkGray
            }
            if ($files.Count -gt 25) { Write-Info "       ... 외 $($files.Count - 25) 개" }

            foreach ($name in $Expected) {
                if (-not ($files | Where-Object { $_.Name -ieq $name })) {
                    Write-Bad "     이 폴더에 $name 없음"
                }
            }

            $partial = $files | Where-Object { $_.Length -eq 0 -or $_.Name -match '\.(tmp|part|download|crdownload)$' }
            if ($partial) {
                Write-Bad "     미완성 파일 $($partial.Count) 개 (다운로드가 끊겼습니다)"
                foreach ($x in ($partial | Select-Object -First 5)) { Write-Info "       $($x.Name)" }
                $Result.Add('bin 폴더에 미완성 다운로드 파일 존재')
            }
        }

        if ($dirs.Count -gt 1) {
            Write-Host ''
            Write-Warn '버전 폴더가 여러 개입니다.'
            Write-Info '앱이 최신 폴더를 보는데 그 안에 구성요소가 없으면 "찾을 수 없음"이 납니다.'
            Write-Info '(구버전 폴더에 파일이 있어도 앱은 그것을 쓰지 않습니다)'
            $Result.Add('bin 버전 폴더가 여러 개 - 앱이 보는 폴더와 파일 위치 불일치 가능')
        }
    }
}

# --------------------------------- 3. 앱 로그에서 오류 문구 추출
Write-Section '3. 앱 로그에서 실제 오류 문구 추출'

$LogRoots = @(
    (Join-PathSafe $env:LOCALAPPDATA 'OpenAI'),
    (Join-PathSafe $env:APPDATA      'OpenAI'),
    (Join-PathSafe $env:LOCALAPPDATA 'ChatGPT'),
    (Join-PathSafe $env:APPDATA      'ChatGPT'),
    (Join-PathSafe $env:USERPROFILE  '.codex')
) | Where-Object { $_ -and (Test-Path $_) } | Select-Object -Unique

if ($LogRoots.Count -eq 0) {
    Write-Warn '앱 데이터 폴더를 찾지 못했습니다.'
} else {
    foreach ($r in $LogRoots) { Write-Info "검색 대상: $r" }

    $logFiles = @()
    foreach ($r in $LogRoots) {
        $f = Get-ChildItem -Path $r -Include *.log,*.txt,*.jsonl,*.ndjson -Recurse -File -Force -ErrorAction SilentlyContinue |
             Where-Object { $_.LastWriteTime -gt (Get-Date).AddDays(-7) -and $_.Length -lt 50MB }
        $logFiles += $f
    }
    $logFiles = $logFiles | Sort-Object LastWriteTime -Descending | Select-Object -First 40

    if ($logFiles.Count -eq 0) {
        Write-Warn '최근 7일 내 로그 파일을 찾지 못했습니다.'
    } else {
        Write-Info "로그 파일 $($logFiles.Count) 개 검사 중..."
        $pattern = 'code-mode-host|computer-use|ENOENT|spawn|not found|failed to (start|launch|spawn)|missing'
        $total = 0

        foreach ($lf in $logFiles) {
            try {
                $hits = Select-String -Path $lf.FullName -Pattern $pattern -ErrorAction SilentlyContinue |
                        Select-Object -Last 6
                if ($hits) {
                    Write-Host ''
                    Write-Host "   $($lf.Name)  ($($lf.LastWriteTime))" -ForegroundColor Yellow
                    foreach ($h in $hits) {
                        $line = $h.Line.Trim()
                        if ($line.Length -gt 200) { $line = $line.Substring(0, 200) + '...' }
                        Write-Host "     $line" -ForegroundColor DarkGray
                        $total++
                    }
                }
            } catch { }
        }

        if ($total -eq 0) {
            Write-Ok '로그에서 관련 오류 문구를 찾지 못했습니다.'
            Write-Info '=> 오류가 해소되었거나, 로그가 초기화되었습니다.'
        } else {
            Write-Host ''
            Write-Warn "총 $total 건의 관련 로그 항목을 찾았습니다. 위 내용을 캡처해 공유하세요."
            $Result.Add("앱 로그에 관련 오류 $total 건")
        }
    }
}

# ------------------------------------------------------- 4. 결론
Write-Section '결론'

if ($Result.Count -eq 0) {
    Write-Ok '이상 징후가 발견되지 않았습니다.'
    Write-Host ''
    Write-Host '  => 앱을 실행하고 .pptx 생성을 다시 요청해 보세요.' -ForegroundColor White
} else {
    Write-Host '  발견 사항:' -ForegroundColor Yellow
    $i = 1
    foreach ($r in $Result) { Write-Host "    $i) $r" -ForegroundColor Yellow; $i++ }
    Write-Host ''
    if ($Result -match '누락|미완성|재설치|비어 있음|불일치') {
        Write-Host '  => 설치 구성요소가 불완전합니다. 재설치가 필요합니다.' -ForegroundColor White
        Write-Host '     1) 앱 완전 종료 (이 스크립트를 -Clean 으로 실행)' -ForegroundColor Gray
        Write-Host '     2) 설정 > 앱 에서 ChatGPT 제거' -ForegroundColor Gray
        Write-Host '     3) 아래 폴더를 통째로 삭제 (앱 설정이 초기화됩니다)' -ForegroundColor Gray
        Write-Host ("        " + (Join-PathSafe $env:LOCALAPPDATA 'OpenAI')) -ForegroundColor Gray
        Write-Host '     4) 공식 페이지에서 다시 받아 관리자 권한으로 설치' -ForegroundColor Gray
        Write-Host '     * 설치 중 V3 실시간 검사를 잠시 꺼두면 재발을 막을 수 있습니다.' -ForegroundColor Gray
    } else {
        Write-Host '  => 이 스크립트를 -Clean 옵션으로 실행한 뒤 앱을 새로 켜세요.' -ForegroundColor White
    }
}

Write-Host ''
Write-Host '  ※ 증상이 재발하면 아래만 실행하면 됩니다:' -ForegroundColor Magenta
Write-Host "     powershell -ExecutionPolicy Bypass -File `"$PSCommandPath`" -Clean" -ForegroundColor Cyan
Write-Host ''
