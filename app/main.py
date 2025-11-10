from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import Base, engine, get_db

# Создаём таблицы при запуске
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Incidents API",
    description="API сервис для учёта инцидентов",
    version="1.0.0"
)


@app.post("/incidents", response_model=schemas.IncidentResponse, status_code=201)
def create_incident(incident: schemas.IncidentCreate, db: Session = Depends(get_db)):
    """Создать новый инцидент"""
    return crud.create_incident(db=db, incident=incident)


@app.get("/incidents", response_model=schemas.IncidentListResponse)
def get_incidents(
    status: Optional[models.IncidentStatus] = Query(None, description="Фильтр по статусу"),
    skip: int = Query(0, ge=0, description="Количество пропущенных записей"),
    limit: int = Query(100, ge=1, le=1000, description="Максимальное количество записей"),
    db: Session = Depends(get_db)
):
    """Получить список инцидентов с фильтром по статусу"""
    incidents, total = crud.get_incidents(db=db, status=status, skip=skip, limit=limit)
    return schemas.IncidentListResponse(items=incidents, total=total)


@app.patch("/incidents/{incident_id}/status", response_model=schemas.IncidentResponse)
def update_incident_status(
    incident_id: int,
    update: schemas.IncidentUpdate,
    db: Session = Depends(get_db)
):
    """Обновить статус инцидента по ID"""
    incident = crud.update_incident_status(db=db, incident_id=incident_id, new_status=update.status)
    if incident is None:
        raise HTTPException(status_code=404, detail="Инцидент не найден")
    return incident


@app.get("/health")
def health_check():
    """Проверка здоровья сервиса"""
    return {"status": "ok"}
