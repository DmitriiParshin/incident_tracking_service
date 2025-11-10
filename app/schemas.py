from datetime import datetime

from pydantic import BaseModel, Field

from app.models import IncidentSource, IncidentStatus


class IncidentCreate(BaseModel):
    """Схема для создания инцидента"""
    description: str = Field(..., description="Описание инцидента")
    source: IncidentSource = Field(..., description="Источник инцидента")


class IncidentUpdate(BaseModel):
    """Схема для обновления статуса инцидента"""
    status: IncidentStatus = Field(..., description="Новый статус инцидента")


class IncidentResponse(BaseModel):
    """Схема ответа с данными инцидента"""
    id: int
    description: str
    status: IncidentStatus
    source: IncidentSource
    created_at: datetime

    class Config:
        from_attributes = True


class IncidentListResponse(BaseModel):
    """Схема ответа со списком инцидентов"""
    items: list[IncidentResponse]
    total: int

