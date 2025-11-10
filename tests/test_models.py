from sqlalchemy.orm import Session

from app.models import Incident, IncidentSource, IncidentStatus


def test_incident_model_creation(test_db: Session):
    """Тест создания модели инцидента"""
    incident = Incident(
        description="Тестовый инцидент",
        status=IncidentStatus.NEW,
        source=IncidentSource.OPERATOR
    )

    test_db.add(incident)
    test_db.commit()
    test_db.refresh(incident)

    assert incident.id is not None
    assert incident.description == "Тестовый инцидент"
    assert incident.status == IncidentStatus.NEW
    assert incident.source == IncidentSource.OPERATOR
    assert incident.created_at is not None


def test_incident_default_status(test_db: Session):
    """Тест значения статуса по умолчанию"""
    incident = Incident(
        description="Тестовый инцидент",
        source=IncidentSource.OPERATOR
    )

    test_db.add(incident)
    test_db.commit()
    test_db.refresh(incident)

    assert incident.status == IncidentStatus.NEW
