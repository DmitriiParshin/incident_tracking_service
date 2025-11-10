import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import IncidentSource

# Тестовая база данных SQLite в памяти
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Переопределение зависимости базы данных для тестов"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def create_tables():
    """Автоматически создает таблицы перед каждым тестом"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def test_db():
    """Фикстура для тестовой базы данных"""
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    # Очищаем таблицы после теста
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    """Фикстура для тестового клиента"""
    # Переопределяем зависимость базы данных
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    # Восстанавливаем оригинальную зависимость
    app.dependency_overrides.clear()


@pytest.fixture
def sample_incident_data():
    """Фикстура с тестовыми данными инцидента"""
    return {
        "description": "Тестовый инцидент",
        "source": IncidentSource.OPERATOR
    }


@pytest.fixture
def sample_incident_data_2():
    """Второй тестовый инцидент"""
    return {
        "description": "Второй тестовый инцидент",
        "source": IncidentSource.MONITORING
    }
