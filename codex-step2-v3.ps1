#Requires -Version 5.1
<#
.SYNOPSIS
    2단계 진단 - codex-code-mode-host.exe 가 "존재하는데 실행되지 않는" 원인 확정

.DESCRIPTION
    1단계에서 실행 파일이 디스크에 정상 존재함이 확인되었습니다.
    따라서 원인은 "파일 누락"이 아니라 "실행 차단"입니다.
    이 스크립트는 exe 를 직접 실행해 Windows 가 반환하는 실제 오류 코드를 받아내고,
    AhnLab V3 로그에서 차단 기록을 찾아 원인을 확정합니다.

.PARAMETER Restart
    정체된 ChatGPT / codex 프로세스를 모두 종료합니다.
    (트레이 아이콘으로는 잘 정리되지 않는 잔여 프로세스를 정리)

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\codex-step2-v3.ps1

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\codex-step2-v3.ps1 -Restart
#>

[CmdletBinding()]
param([switch]$Restart)

$ErrorActionPreference = 'Continue'
$ProgressPreference    = 'SilentlyContinue'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch { }

$TargetExe = 'codex-code-mode-host.exe'
$Verdict   = [System.Collections.Generic.List[string]]::new()
$ForIT     = [System.Collections.Generic.List[string]]::new()

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

Clear-Host
Write-Host ''
Write-Host '  2단계 - 실행 차단 원인 확정' -ForegroundColor White
Write-Host '  ---------------------------' -ForegroundColor DarkGray

# ------------------------------------------------- 1. exe 다시 찾기
Write-Section "1. $TargetExe 위치 및 상태"

$Roots = @(
    (Join-PathSafe $env:LOCALAPPDATA 'Programs'),
    $env:LOCALAPPDATA, $env:APPDATA, $env:ProgramFiles,
    ${env:ProgramFiles(x86)}, $env:ProgramData
) | Where-Object { $_ -and (Test-Path $_) } | Select-Object -Unique

$Exe = $null
foreach ($r in $Roots) {
    $hit = Get-ChildItem -Path $r -Filter $TargetExe -Recurse -File -Force -ErrorAction SilentlyContinue |
           Select-Object -First 1
    if ($hit) { $Exe = $hit; break }
}

if (-not $Exe) {
    Write-Bad "$TargetExe 를 찾지 못했습니다. 1단계 결과와 다릅니다 - 그 사이 삭제되었을 수 있습니다."
    Write-Info 'V3 가 방금 이 파일을 격리했을 가능성이 있습니다. V3 격리소를 확인하세요.'
    $Verdict.Add('실행 파일이 사라짐 - V3 격리 의심')
} else {
    Write-Ok "경로 : $($Exe.FullName)"
    Write-Info ("크기 : {0:N0} bytes" -f $Exe.Length)
    Write-Info ("수정 : $($Exe.LastWriteTime)")
    try {
        $h = Get-FileHash -Path $Exe.FullName -Algorithm SHA256 -ErrorAction Stop
        Write-Info "SHA256: $($h.Hash)"
        $ForIT.Add("SHA256: $($h.Hash)")
    } catch { }
    try {
        $sig = Get-AuthenticodeSignature -FilePath $Exe.FullName -ErrorAction Stop
        $signer = if ($sig.SignerCertificate) { $sig.SignerCertificate.Subject -replace '^CN=([^,]+).*','$1' } else { '(없음)' }
        if ($sig.Status -eq 'Valid') { Write-Ok "서명 : 정상 / 발급대상 $signer" }
        else { Write-Warn "서명 : $($sig.Status) / $signer" }
        $ForIT.Add("서명: $($sig.Status) / $signer")
    } catch { }
    $ForIT.Add("경로: $($Exe.FullName)")
}

# --------------------------------------- 2. 직접 실행 테스트 (핵심)
Write-Section '2. 직접 실행 테스트 - 실제 오류 코드 확인'

if (-not $Exe) {
    Write-Info '실행 파일이 없어 건너뜁니다.'
} else {
    Write-Info '보조 프로세스를 잠시 띄웠다가 즉시 종료합니다. (최대 6초)'
    $outFile = Join-Path $env:TEMP 'codex_host_out.txt'
    $errFile = Join-Path $env:TEMP 'codex_host_err.txt'
    $blocked = $false

    try {
        $p = Start-Process -FilePath $Exe.FullName -PassThru `
                           -RedirectStandardOutput $outFile -RedirectStandardError $errFile `
                           -ErrorAction Stop
        Write-Ok "프로세스가 기동되었습니다. (PID $($p.Id))"
        Write-Info '=> Windows 수준에서 실행이 차단되고 있지는 않습니다.'

        $exited = $p.WaitForExit(6000)
        if ($exited) {
            Write-Warn "프로세스가 스스로 종료되었습니다. 종료 코드: $($p.ExitCode)"
            if ($p.ExitCode -ne 0) {
                $Verdict.Add("보조 프로세스가 비정상 종료 (코드 $($p.ExitCode))")
            } else {
                Write-Info '정상 종료 코드입니다. 단독 실행 시에는 정상 동작으로 보입니다.'
            }
        } else {
            Write-Ok '6초간 정상 대기 상태를 유지했습니다. exe 자체는 건강합니다.'
            try { $p.Kill(); Write-Info '테스트 프로세스를 정리했습니다.' } catch { }
        }

        foreach ($f in @(@{P=$errFile;L='표준 오류'}, @{P=$outFile;L='표준 출력'})) {
            if (Test-Path $f.P) {
                $t = (Get-Content $f.P -Raw -ErrorAction SilentlyContinue)
                if ($t -and $t.Trim()) {
                    Write-Warn "$($f.L):"
                    Write-Host ($t.Trim()) -ForegroundColor DarkGray
                    $ForIT.Add("$($f.L): $($t.Trim())")
                }
            }
        }
    } catch {
        $msg = $_.Exception.Message
        # Win32 예외일 때만 "차단"으로 단정한다.
        # 그 외(파라미터 문제 등)는 차단과 무관하므로 오진하지 않는다.
        $win32 = $null
        if ($_.Exception.InnerException -is [System.ComponentModel.Win32Exception]) {
            $win32 = $_.Exception.InnerException
        } elseif ($_.Exception -is [System.ComponentModel.Win32Exception]) {
            $win32 = $_.Exception
        }

        if ($win32) {
            $blocked = $true
            $code = $win32.NativeErrorCode
            Write-Bad '실행이 거부되었습니다. <== 앱이 보고한 "누락 오류"의 실체입니다.'
            Write-Host "  오류: $msg" -ForegroundColor Red
            Write-Host "  Win32 오류 코드: $code" -ForegroundColor Red
            $ForIT.Add("실행 거부: $msg (Win32 코드 $code)")
            switch ($code) {
                5    { Write-Bad '  코드 5 (액세스 거부) - 보안 소프트웨어가 실행을 막고 있습니다.'
                       $Verdict.Add('보안 소프트웨어가 exe 실행을 차단함 (액세스 거부)') }
                2    { Write-Bad '  코드 2 (파일을 찾을 수 없음) - 실행 직전에 파일이 치워졌습니다.'
                       $Verdict.Add('실행 시점에 파일이 사라짐 - 실시간 감시가 치우는 중') }
                1260 { Write-Bad '  코드 1260 - 그룹 정책/응용프로그램 제어로 차단되었습니다.'
                       $Verdict.Add('그룹 정책 또는 응용프로그램 제어가 실행을 차단함') }
                default { Write-Bad "  코드 $code"
                          $Verdict.Add("exe 실행 실패 (Win32 코드 $code)") }
            }
        } else {
            Write-Warn '실행 테스트를 수행하지 못했습니다. (차단과는 다른 종류의 오류입니다)'
            Write-Host "  오류: $msg" -ForegroundColor DarkGray
            Write-Info '=> 이것만으로는 차단 여부를 판단할 수 없습니다. 아래 3번 항목을 확인하세요.'
            $ForIT.Add("실행 테스트 실패: $msg")
        }
    }

    Remove-Item $outFile, $errFile -Force -ErrorAction SilentlyContinue
}

# ------------------------------------ 3. AhnLab V3 차단 기록 확인
Write-Section '3. AhnLab V3 설치 상태 및 차단 기록'

$AhnRoots = @(
    (Join-PathSafe $env:ProgramFiles 'AhnLab'),
    (Join-PathSafe ${env:ProgramFiles(x86)} 'AhnLab'),
    (Join-PathSafe $env:ProgramData 'AhnLab')
) | Where-Object { $_ -and (Test-Path $_) }

if ($AhnRoots.Count -eq 0) {
    Write-Info 'AhnLab 설치 폴더를 찾지 못했습니다.'
} else {
    foreach ($a in $AhnRoots) { Write-Ok "설치 폴더: $a" }

    $v3proc = Get-Process -ErrorAction SilentlyContinue |
              Where-Object { $_.ProcessName -match '(?i)^(v3|asd|ahn)' }
    if ($v3proc) {
        Write-Info '실행 중인 V3 프로세스:'
        foreach ($p in ($v3proc | Select-Object -First 8)) {
            Write-Info "  $($p.ProcessName) (PID $($p.Id))"
        }
    }

    Write-Info '로그에서 codex 관련 차단 기록을 검색합니다... (시간이 걸릴 수 있습니다)'
    $found = 0
    foreach ($a in $AhnRoots) {
        $logs = Get-ChildItem -Path $a -Include *.log,*.txt,*.csv -Recurse -File -Force -ErrorAction SilentlyContinue |
                Where-Object { $_.LastWriteTime -gt (Get-Date).AddDays(-14) } |
                Select-Object -First 200
        foreach ($l in $logs) {
            try {
                $m = Select-String -Path $l.FullName -Pattern 'codex' -SimpleMatch -ErrorAction SilentlyContinue |
                     Select-Object -First 3
                foreach ($x in $m) {
                    if ($found -eq 0) { Write-Bad 'V3 로그에서 codex 관련 기록이 발견되었습니다:' }
                    $found++
                    Write-Host "  $($l.Name): $($x.Line.Trim())" -ForegroundColor Yellow
                    $ForIT.Add("V3 로그: $($x.Line.Trim())")
                }
            } catch { }
        }
    }
    if ($found -eq 0) {
        Write-Info '읽을 수 있는 로그에서는 codex 기록을 찾지 못했습니다.'
        Write-Info '(V3 로그는 암호화/잠금되는 경우가 많아 V3 화면에서 직접 확인이 필요합니다)'
    } else {
        $Verdict.Add("V3 로그에 codex 관련 차단 기록 $found 건")
    }
}

# --------------------------------- 4. 정체된 앱 프로세스 정리
Write-Section '4. 정체된 앱 프로세스 정리'

$stale = Get-Process -ErrorAction SilentlyContinue |
         Where-Object { $_.ProcessName -match '(?i)^(chatgpt|codex)' }

if (-not $stale) {
    Write-Ok '실행 중인 ChatGPT / codex 프로세스가 없습니다.'
} else {
    Write-Warn "실행 중인 관련 프로세스 $($stale.Count) 개"
    if (-not $Restart) {
        Write-Info '-Restart 옵션을 붙이면 모두 종료합니다. (앱 재시작 전 권장)'
        Write-Info '진행 중인 대화가 있다면 먼저 저장하세요.'
    } else {
        foreach ($p in $stale) {
            try { $p.Kill(); Write-Info "종료: $($p.ProcessName) (PID $($p.Id))" }
            catch { Write-Warn "종료 실패: $($p.ProcessName) (PID $($p.Id))" }
        }
        Start-Sleep -Seconds 2
        $left = Get-Process -ErrorAction SilentlyContinue |
                Where-Object { $_.ProcessName -match '(?i)^(chatgpt|codex)' }
        if ($left) { Write-Warn "$($left.Count) 개가 남아 있습니다. 재부팅이 필요할 수 있습니다." }
        else { Write-Ok '모든 관련 프로세스를 정리했습니다. 이제 앱을 새로 실행하세요.' }
    }
}

# ------------------------------------------------------- 5. 결론
Write-Section '결론'

if ($Verdict.Count -eq 0) {
    Write-Ok 'exe 는 정상이고 실행 차단 증거도 발견되지 않았습니다.'
    Write-Host ''
    Write-Host '  => 남은 원인은 "정체된 프로세스"일 가능성이 큽니다.' -ForegroundColor White
    Write-Host '     아래 순서로 진행하세요:' -ForegroundColor White
    Write-Host '       1) 이 스크립트를 -Restart 옵션으로 다시 실행' -ForegroundColor Gray
    Write-Host '       2) 앱을 새로 실행' -ForegroundColor Gray
    Write-Host '       3) 대화창에 ".pptx 파일로 만들어줘" 재요청' -ForegroundColor Gray
} else {
    Write-Host '  확정된 사실:' -ForegroundColor Yellow
    $i = 1
    foreach ($v in $Verdict) { Write-Host "    $i) $v" -ForegroundColor Yellow; $i++ }
    Write-Host ''
    Write-Host '  => AhnLab V3 화면에서 아래를 확인하세요:' -ForegroundColor White
    Write-Host '     - 격리소 / 검역소에 codex 관련 항목이 있으면 [복원]' -ForegroundColor Gray
    Write-Host '     - 차단 기록 / 보안 로그에서 codex 항목 확인' -ForegroundColor Gray
    Write-Host '     - 위 exe 경로를 검사 제외(예외) 목록에 추가' -ForegroundColor Gray
}

Write-Host ''
Write-Host '  ※ V3 Endpoint Security 는 기관에서 중앙 관리하는 제품입니다.' -ForegroundColor Magenta
Write-Host '    설정이 잠겨 있으면 학교 정보 담당 선생님께 아래 정보를 전달하세요.' -ForegroundColor Magenta

if ($ForIT.Count -gt 0) {
    Write-Host ''
    Write-Host '  --- IT 담당자 전달용 정보 ---' -ForegroundColor White
    foreach ($f in $ForIT) { Write-Host "    $f" -ForegroundColor Gray }
    Write-Host '    요청 내용: 위 실행 파일을 V3 검사 제외 목록에 추가해 주세요.' -ForegroundColor Gray
    Write-Host '  ---------------------------' -ForegroundColor White
}
Write-Host ''
