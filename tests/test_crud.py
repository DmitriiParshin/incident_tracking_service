from sqlalchemy.orm import Session

from app import crud
from app.models import IncidentStatus
from app.schemas import IncidentCreate


def test_create_incident(test_db: Session, sample_incident_data):
    """Тест создания инцидента через CRUD"""
    incident_create = IncidentCreate(**sample_incident_data)
    incident = crud.create_incident(test_db, incident_create)

    assert incident.id is not None
    assert incident.description == sample_incident_data["description"]
    assert incident.source == sample_incident_data["source"]
    assert incident.status == IncidentStatus.NEW


def test_get_incident_by_id(test_db: Session, sample_incident_data):
    """Тест получения инцидента по ID"""
    incident_create = IncidentCreate(**sample_incident_data)
    created_incident = crud.create_incident(test_db, incident_create)

    retrieved_incident = crud.get_incident_by_id(test_db, created_incident.id)

    assert retrieved_incident is not None
    assert retrieved_incident.id == created_incident.id
    assert retrieved_incident.description == created_incident.description


def test_get_incident_by_id_not_found(test_db: Session):
    """Тест получения несуществующего инцидента"""
    incident = crud.get_incident_by_id(test_db, 999)
    assert incident is None


def test_get_incidents_empty(test_db: Session):
    """Тест получения пустого списка инцидентов"""
    incidents, total = crud.get_incidents(test_db)
    assert len(incidents) == 0
    assert total == 0


def test_get_incidents_with_data(test_db: Session, sample_incident_data, sample_incident_data_2):
    """Тест получения списка инцидентов"""
    # Создаем два инцидента
    incident1 = crud.create_incident(test_db, IncidentCreate(**sample_incident_data))
    incident2 = crud.create_incident(test_db, IncidentCreate(**sample_incident_data_2))

    incidents, total = crud.get_incidents(test_db)

    assert total == 2
    assert len(incidents) == 2
    incident_ids = [incident.id for incident in incidents]
    assert incident1.id in incident_ids
    assert incident2.id in incident_ids


def test_get_incidents_with_status_filter(test_db: Session, sample_incident_data):
    """Тест фильтрации инцидентов по статусу"""
    # Создаем инцидент со статусом NEW
    incident_new = crud.create_incident(test_db, IncidentCreate(**sample_incident_data))

    # Обновляем статус инцидента
    crud.update_incident_status(test_db, incident_new.id, IncidentStatus.IN_PROGRESS)

    # Получаем инциденты с разными статусами
    new_incidents, new_total = crud.get_incidents(test_db, status=IncidentStatus.NEW)
    in_progress_incidents, in_progress_total = crud.get_incidents(test_db, status=IncidentStatus.IN_PROGRESS)

    assert new_total == 0
    assert len(new_incidents) == 0
    assert in_progress_total == 1
    assert len(in_progress_incidents) == 1
    assert in_progress_incidents[0].status == IncidentStatus.IN_PROGRESS


def test_update_incident_status(test_db: Session, sample_incident_data):
    """Тест обновления статуса инцидента"""
    incident_create = IncidentCreate(**sample_incident_data)
    incident = crud.create_incident(test_db, incident_create)

    # Обновляем статус
    updated_incident = crud.update_incident_status(
        test_db, incident.id, IncidentStatus.RESOLVED
    )

    assert updated_incident is not None
    assert updated_incident.id == incident.id
    assert updated_incident.status == IncidentStatus.RESOLVED


def test_update_incident_status_not_found(test_db: Session):
    """Тест обновления статуса несуществующего инцидента"""
    updated_incident = crud.update_incident_status(
        test_db, 999, IncidentStatus.RESOLVED
    )

    assert updated_incident is None


def test_get_incidents_pagination(test_db: Session, sample_incident_data):
    """Тест пагинации списка инцидентов"""
    # Создаем несколько инцидентов
    incidents_data = []
    for i in range(5):
        incident_data = sample_incident_data.copy()
        incident_data["description"] = f"Инцидент {i}"
        incidents_data.append(incident_data)

    # Создаем инциденты
    created_incidents = []
    for data in incidents_data:
        incident = crud.create_incident(test_db, IncidentCreate(**data))
        created_incidents.append(incident)

    # Тестируем пагинацию
    incidents_page1, total_page1 = crud.get_incidents(test_db, skip=0, limit=2)
    incidents_page2, total_page2 = crud.get_incidents(test_db, skip=2, limit=2)

    assert total_page1 == 5
    assert total_page2 == 5
    assert len(incidents_page1) == 2
    assert len(incidents_page2) == 2
    # Проверяем, что на разных страницах разные инциденты
    assert incidents_page1[0].id != incidents_page2[0].id
