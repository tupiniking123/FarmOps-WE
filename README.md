# FarmSaaS

Projeto SaaS agrícola com duas frentes:

- **Nova base SaaS cross-platform**: `backend/` + `mobile_flutter/` (Windows e Android).
- **Distribuição desktop Windows existente**: `packaging/windows/` para launcher Streamlit (`FarmSaaS.exe`).

## Quick start

### Backend API
```bash
pip install -r backend/requirements_backend.txt
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

### App Flutter
```bash
cd mobile_flutter
flutter pub get
flutter run -d windows
```

### Build Windows launcher (Streamlit legado)
```powershell
powershell -ExecutionPolicy Bypass -File packaging/windows/build_exe.ps1
```
