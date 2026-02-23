diff --git a/packaging/windows/README_WINDOWS_BUILD.md b/packaging/windows/README_WINDOWS_BUILD.md
new file mode 100644
index 0000000000000000000000000000000000000000..577664801fdf2950570f97c67c85e2d4c569de48
--- /dev/null
+++ b/packaging/windows/README_WINDOWS_BUILD.md
@@ -0,0 +1,48 @@
+# Build Windows - FarmSaaS Rural
+
+Este guia gera um launcher desktop (`FarmSaaS.exe`) para executar o Streamlit com 1 clique.
+
+## Pré-requisitos (máquina de build)
+- Windows 10/11
+- Python 3.10+
+- PowerShell
+- (Opcional) Inno Setup 6 para criar instalador
+
+## Estrutura gerada
+- `dist/FarmSaaS/FarmSaaS.exe`
+- `dist/FarmSaaS/logs/app.log`
+- `installer/FarmSaaS-Setup.exe` (opcional, via Inno Setup)
+
+## Comando principal
+No diretório raiz do repositório:
+
+```powershell
+powershell -ExecutionPolicy Bypass -File packaging/windows/build_exe.ps1
+```
+
+Esse script:
+1. Cria `.venv-build`
+2. Instala dependências (`requirements_client.txt` + `pyinstaller`)
+3. Garante `client/assets/icon.ico`
+4. Executa PyInstaller com `packaging/windows/FarmSaaS.spec`
+5. Prepara `dist/FarmSaaS/`
+
+## Gerar instalador (opcional)
+1. Abra o Inno Setup.
+2. Carregue `packaging/windows/installer.iss`.
+3. Clique em **Build**.
+
+Saída esperada:
+- `installer/FarmSaaS-Setup.exe`
+
+## Execução do app empacotado
+Ao abrir `FarmSaaS.exe`:
+1. Inicia Streamlit na porta `8501`
+2. Aguarda servidor responder
+3. Abre `http://localhost:8501` no navegador padrão
+4. Mantém o Streamlit ativo em background enquanto o launcher estiver aberto
+5. Ao encerrar o launcher, finaliza o Streamlit
+
+## Solução de problemas
+- Se a porta `8501` estiver ocupada, finalize o processo existente e execute novamente.
+- Consulte logs em `dist/FarmSaaS/logs/app.log`.
