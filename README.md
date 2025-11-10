# Incidents tracking service

API сервис для учёта инцидентов. Позволяет создавать, просматривать и обновлять статусы инцидентов.

## Функциональность

- ✅ Создание инцидентов
- ✅ Получение списка инцидентов с фильтрацией по статусу
- ✅ Обновление статуса инцидента
- ✅ Пагинация и сортировка
- ✅ Валидация данных
- ✅ Полная документация API

## Технологии

- **Python 3.12**
- **FastAPI** - современный, быстрый веб-фреймворк
- **SQLAlchemy** - ORM для работы с базой данных
- **SQLite** - база данных
- **Poetry** - управление зависимостями
- **Docker** - контейнеризация
- **Pytest** - тестирование
- **Ruff** - линтинг и форматирование кода

## Быстрый старт

### Локальная установка

1. **Клонируйте репозиторий:**
```
git clone git@github.com:DmitriiParshin/incident_tracking_service.git
cd incident_tracking_service
```

2. **Запуск сервиса в Docker:**
```
docker compose up -d
```

3. **Запуск тестов в Docker:**
```
docker compose run tests
```

### Примеры использования

1. **Создание инцидента**
```
curl -X POST "http://localhost:8000/incidents/" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Самокат не в сети более 2 часов",
    "source": "monitoring"
  }'
```

2. **Получение списка инцидентов**
```
curl "http://localhost:8000/incidents/?status=new&limit=10"
```

3. **Обновление статуса**
```
curl -X PATCH "http://localhost:8000/incidents/1/status" \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}'
```
