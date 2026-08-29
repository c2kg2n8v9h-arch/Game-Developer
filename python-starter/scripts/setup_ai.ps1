param(
    [ValidateSet("runtime", "full")]
    [string]$Profile = "runtime"
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$venvPath = Join-Path $projectRoot ".venv"
$pythonPath = Join-Path $venvPath "Scripts\python.exe"

if (-not (Test-Path -LiteralPath $pythonPath)) {
    python -m venv $venvPath
}

& $pythonPath -m pip install --upgrade pip
$extras = if ($Profile -eq "full") { "dev,ai,optimization,training,media" } else { "dev,ai" }
& $pythonPath -m pip install -e "${projectRoot}[$extras]"
& $pythonPath -m pip check

Write-Host "Hugging Face $Profile stack is ready in $venvPath"
Write-Host "Run: .\.venv\Scripts\python.exe -m rag_service"
