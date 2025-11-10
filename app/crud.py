from typing import Optional

from sqlalchemy.orm import Session

from app import models, schemas


def create_incident(db: Session, incident: schemas.IncidentCreate) -> models.Incident:
    """Создать новый инцидент"""
    db_incident = models.Incident(
        description=incident.description,
        source=incident.source,
        status=models.IncidentStatus.NEW
    )
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident


def get_incidents(
    db: Session,
    status: Optional[models.IncidentStatus] = None,
    skip: int = 0,
    limit: int = 100
) -> tuple[list[type[models.Incident]], int]:
    """Получить список инцидентов с фильтром по статусу"""
    query = db.query(models.Incident)

    if status is not None:
        query = query.filter(models.Incident.status == status)

    total = query.count()
    incidents = query.order_by(models.Incident.created_at.desc()).offset(skip).limit(limit).all()

    return incidents, total


def get_incident_by_id(db: Session, incident_id: int) -> Optional[models.Incident]:
    """Получить инцидент по ID"""
    return db.query(models.Incident).filter(models.Incident.id == incident_id).first()


def update_incident_status(
    db: Session,
    incident_id: int,
    new_status: models.IncidentStatus
) -> Optional[models.Incident]:
    """Обновить статус инцидента"""
    db_incident = get_incident_by_id(db, incident_id)
    if db_incident is None:
        return None

    db_incident.status = new_status
    db.commit()
    db.refresh(db_incident)
    return db_incident

