# FarmSaaS - Arquitetura SaaS (Windows + Android)

## Stack avançada proposta
- **Backend SaaS**: FastAPI + SQLModel (multi-tenant leve via `tenant_id`)
- **App cliente cross-platform**: Flutter (Dart) para **Windows Desktop e Android**
- **Empacotamento Windows legado**: PyInstaller/Inno Setup (mantido em `packaging/windows/`)

## Componentes
1. `backend/app/main.py`
   - API REST para health, tenants, farms e activities.
2. `mobile_flutter/`
   - App Flutter único para Windows e Android consumindo a API.
3. `packaging/windows/`
   - Pipeline para gerar executável instalável no Windows (modo Streamlit legado).

## Como executar (dev)
### Backend
```bash
python -m venv .venv
. .venv/bin/activate
pip install -r backend/requirements_backend.txt
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Flutter (Windows/Android)
```bash
cd mobile_flutter
flutter pub get
flutter run -d windows
# ou
flutter run -d android
```

## Evolução para SaaS real
- Adicionar autenticação JWT + RBAC.
- Migrar SQLite para PostgreSQL gerenciado.
- Adicionar billing (Stripe/Pagar.me) por tenant.
- Deploy cloud do backend (AWS/Azure/GCP) + CI/CD.
