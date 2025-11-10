from fastapi.testclient import TestClient

from app.models import IncidentStatus


def test_health_check(client: TestClient):
    """Тест эндпоинта проверки здоровья"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_incident(client: TestClient, sample_incident_data):
    """Тест создания инцидента через API"""
    response = client.post("/incidents/", json=sample_incident_data)

    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["description"] == sample_incident_data["description"]
    assert data["source"] == sample_incident_data["source"]
    assert data["status"] == IncidentStatus.NEW
    assert "created_at" in data


def test_create_incident_invalid_data(client: TestClient):
    """Тест создания инцидента с невалидными данными"""
    invalid_data = {
        "description": "",  # Пустое описание
        "source": "invalid_source"  # Невалидный источник
    }

    response = client.post("/incidents/", json=invalid_data)
    assert response.status_code == 422  # Validation error


def test_get_incidents_empty(client: TestClient):
    """Тест получения пустого списка инцидентов"""
    response = client.get("/incidents/")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert len(data["items"]) == 0


def test_get_incidents_with_data(client: TestClient, sample_incident_data, sample_incident_data_2):
    """Тест получения списка инцидентов"""
    # Создаем два инцидента
    client.post("/incidents/", json=sample_incident_data)
    client.post("/incidents/", json=sample_incident_data_2)

    response = client.get("/incidents/")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

    # Проверяем сортировку (последний созданный первый)
    assert data["items"][0]["source"] == "operator"
    assert data["items"][1]["source"] == "monitoring"


def test_get_incidents_with_status_filter(client: TestClient, sample_incident_data):
    """Тест фильтрации инцидентов по статусу"""
    # Создаем инцидент
    create_response = client.post("/incidents/", json=sample_incident_data)
    incident_id = create_response.json()["id"]

    # Получаем инциденты со статусом NEW
    response_new = client.get("/incidents/", params={"status": "new"})
    assert response_new.status_code == 200
    assert response_new.json()["total"] == 1

    # Обновляем статус
    update_data = {"status": "in_progress"}
    client.patch(f"/incidents/{incident_id}/status", json=update_data)

    # Проверяем фильтрацию
    response_new_after_update = client.get("/incidents/", params={"status": "new"})
    response_in_progress = client.get("/incidents/", params={"status": "in_progress"})

    assert response_new_after_update.json()["total"] == 0
    assert response_in_progress.json()["total"] == 1


def test_get_incidents_pagination(client: TestClient, sample_incident_data):
    """Тест пагинации списка инцидентов"""
    # Создаем несколько инцидентов
    for i in range(5):
        data = sample_incident_data.copy()
        data["description"] = f"Инцидент {i}"
        client.post("/incidents/", json=data)

    # Тестируем пагинацию
    response_page1 = client.get("/incidents/", params={"skip": 0, "limit": 2})
    response_page2 = client.get("/incidents/", params={"skip": 2, "limit": 2})

    assert response_page1.status_code == 200
    assert response_page2.status_code == 200

    page1_data = response_page1.json()
    page2_data = response_page2.json()

    assert page1_data["total"] == 5
    assert len(page1_data["items"]) == 2
    assert len(page2_data["items"]) == 2
    assert page1_data["items"][0]["id"] != page2_data["items"][0]["id"]


def test_update_incident_status_success(client: TestClient, sample_incident_data):
    """Тест успешного обновления статуса инцидента"""
    # Создаем инцидент
    create_response = client.post("/incidents/", json=sample_incident_data)
    incident_id = create_response.json()["id"]

    # Обновляем статус
    update_data = {"status": IncidentStatus.RESOLVED}
    response = client.patch(f"/incidents/{incident_id}/status", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == IncidentStatus.RESOLVED
    assert data["id"] == incident_id


def test_update_incident_status_not_found(client: TestClient):
    """Тест обновления статуса несуществующего инцидента"""
    update_data = {"status": IncidentStatus.RESOLVED}
    response = client.patch("/incidents/999/status", json=update_data)

    assert response.status_code == 404
    assert response.json()["detail"] == "Инцидент не найден"


def test_update_incident_status_invalid_data(client: TestClient, sample_incident_data):
    """Тест обновления статуса с невалидными данными"""
    # Создаем инцидент
    create_response = client.post("/incidents/", json=sample_incident_data)
    incident_id = create_response.json()["id"]

    # Пытаемся обновить с невалидным статусом
    invalid_data = {"status": "invalid_status"}
    response = client.patch(f"/incidents/{incident_id}/status", json=invalid_data)

    assert response.status_code == 422
