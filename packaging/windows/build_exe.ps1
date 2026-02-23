$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "../..")
$VenvDir = Join-Path $RepoRoot ".venv-build"
$DistRoot = Join-Path $RepoRoot "dist"
$WorkDist = Join-Path $DistRoot "FarmSaaS"
$IconPath = Join-Path $RepoRoot "client/assets/icon.ico"

Write-Host "[1/6] Preparando ambiente virtual..."
if (-not (Test-Path $VenvDir)) {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        py -3 -m venv $VenvDir
    }
    else {
        python -m venv $VenvDir
    }
}

$PythonExe = Join-Path $VenvDir "Scripts/python.exe"
$PipExe = Join-Path $VenvDir "Scripts/pip.exe"

Write-Host "[2/6] Instalando dependências..."
& $PythonExe -m pip install --upgrade pip
& $PipExe install -r (Join-Path $RepoRoot "requirements_client.txt")
& $PipExe install pyinstaller

Write-Host "[3/6] Garantindo ícone..."
if (-not (Test-Path $IconPath)) {
    & $PythonExe (Join-Path $RepoRoot "packaging/windows/generate_icon.py")
}

Write-Host "[4/6] Build com PyInstaller..."
Push-Location $RepoRoot
& $PythonExe -m PyInstaller --noconfirm --clean (Join-Path $RepoRoot "packaging/windows/FarmSaaS.spec")
Pop-Location

Write-Host "[5/6] Copiando arquivos adicionais..."
New-Item -ItemType Directory -Force -Path $WorkDist | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $WorkDist "logs") | Out-Null

Write-Host "[6/6] Build concluído: $WorkDist"
Write-Host "Executável: $(Join-Path $WorkDist 'FarmSaaS.exe')"
