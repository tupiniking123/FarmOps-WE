from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select

from .database import get_session, init_db
from .models import Activity, Farm, Tenant
from .schemas import ActivityCreate, FarmCreate, HealthResponse, TenantCreate

app = FastAPI(title="FarmSaaS API", version="1.0.0")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", timestamp=datetime.utcnow())


@app.post("/tenants", response_model=Tenant)
def create_tenant(payload: TenantCreate, session: Session = Depends(get_session)) -> Tenant:
    existing = session.exec(select(Tenant).where(Tenant.email == payload.email)).first()
    if existing:
        raise HTTPException(status_code=409, detail="E-mail já cadastrado")
    tenant = Tenant(name=payload.name, email=payload.email)
    session.add(tenant)
    session.commit()
    session.refresh(tenant)
    return tenant


@app.get("/tenants", response_model=list[Tenant])
def list_tenants(session: Session = Depends(get_session)) -> list[Tenant]:
    return list(session.exec(select(Tenant)))


@app.post("/farms", response_model=Farm)
def create_farm(payload: FarmCreate, session: Session = Depends(get_session)) -> Farm:
    tenant = session.get(Tenant, payload.tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant não encontrado")

    farm = Farm(**payload.model_dump())
    session.add(farm)
    session.commit()
    session.refresh(farm)
    return farm


@app.get("/farms/{tenant_id}", response_model=list[Farm])
def list_farms(tenant_id: int, session: Session = Depends(get_session)) -> list[Farm]:
    return list(session.exec(select(Farm).where(Farm.tenant_id == tenant_id)))


@app.post("/activities", response_model=Activity)
def create_activity(payload: ActivityCreate, session: Session = Depends(get_session)) -> Activity:
    tenant = session.get(Tenant, payload.tenant_id)
    farm = session.get(Farm, payload.farm_id)
    if not tenant or not farm:
        raise HTTPException(status_code=404, detail="Tenant/Farm inválido")

    activity = Activity(**payload.model_dump())
    session.add(activity)
    session.commit()
    session.refresh(activity)
    return activity


@app.get("/activities/{tenant_id}", response_model=list[Activity])
def list_activities(tenant_id: int, session: Session = Depends(get_session)) -> list[Activity]:
    return list(session.exec(select(Activity).where(Activity.tenant_id == tenant_id)))
