# Build Windows - FarmSaaS Rural

Este guia gera um launcher desktop (`FarmSaaS.exe`) para executar o Streamlit com 1 clique.

## Pré-requisitos (máquina de build)
- Windows 10/11
- Python 3.10+
- PowerShell
- (Opcional) Inno Setup 6 para criar instalador

## Estrutura gerada
- `dist/FarmSaaS/FarmSaaS.exe`
- `dist/FarmSaaS/logs/app.log`
- `installer/FarmSaaS-Setup.exe` (opcional, via Inno Setup)

## Comando principal
No diretório raiz do repositório:

```powershell
powershell -ExecutionPolicy Bypass -File packaging/windows/build_exe.ps1
```

Esse script:
1. Cria `.venv-build`
2. Instala dependências (`requirements_client.txt` + `pyinstaller`)
3. Gera `client/assets/icon.ico` automaticamente com `packaging/windows/generate_icon.py` (se não existir)
4. Executa PyInstaller com `packaging/windows/FarmSaaS.spec`
5. Prepara `dist/FarmSaaS/`

## Gerar instalador (opcional)
1. Abra o Inno Setup.
2. Carregue `packaging/windows/installer.iss`.
3. Clique em **Build**.

Saída esperada:
- `installer/FarmSaaS-Setup.exe`

## Execução do app empacotado
Ao abrir `FarmSaaS.exe`:
1. Inicia Streamlit na porta `8501`
2. Aguarda servidor responder
3. Abre `http://localhost:8501` no navegador padrão
4. Mantém o Streamlit ativo em background enquanto o launcher estiver aberto
5. Ao encerrar o launcher, finaliza o Streamlit

## Solução de problemas
- Se a porta `8501` estiver ocupada, finalize o processo existente e execute novamente.
- Consulte logs em `dist/FarmSaaS/logs/app.log`.
