FROM python:3.12-slim

WORKDIR /app

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копирование файлов зависимостей
COPY pyproject.toml poetry.lock* ./

# Установка Poetry
RUN pip install poetry

# Настройка Poetry (не создавать виртуальное окружение в контейнере)
RUN poetry config virtualenvs.create false

# Установка зависимостей без установки корневого пакета
RUN poetry install --no-interaction --no-ansi --no-root

# Копирование исходного кода
COPY app/ ./app/
COPY tests/ ./tests/

# Создание директории для базы данных
RUN mkdir -p /app/data

# Открытие порта
EXPOSE 8000

# Запуск приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]