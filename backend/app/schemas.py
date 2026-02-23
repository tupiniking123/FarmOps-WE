from datetime import datetime
from pydantic import BaseModel


class TenantCreate(BaseModel):
    name: str
    email: str


class FarmCreate(BaseModel):
    tenant_id: int
    name: str
    city: str
    state: str
    area_hectares: float


class ActivityCreate(BaseModel):
    tenant_id: int
    farm_id: int
    title: str
    notes: str = ""


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
