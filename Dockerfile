# Используем официальный образ Python как базовый образ
FROM python:3.12-slim

# Устанавливаем рабочий каталог для нашего приложения
WORKDIR /app

# Устанавливаем переменные окружения для poetry
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION 1.7.1
ENV POETRY_HOME "/opt/poetry"
ENV POETRY_NO_INTERACTION 1
ENV PATH "$POETRY_HOME/bin:$PATH"

# Устанавливаем poetry
RUN apt-get update

# Обновляем pip
RUN pip install --upgrade pip

# Устанавливаем зависимости Python
RUN pip install "poetry==$POETRY_VERSION"

# Копируем файлы проекта и установки poetry в рабочий каталог
COPY pyproject.toml poetry.lock* /app/

# Копируем исходный код проекта в рабочий каталог
COPY . /app

# Устанавливаем зависимости через poetry, используя флаг --no-root, чтобы не устанавливать сам проект
RUN poetry config virtualenvs.create false \
    && poetry install --only main

RUN ls -la /app
# Команда для запуска приложения
CMD ["poetry", "run", "uvicorn", "src.WidgetGen.main:app", "--host", "0.0.0.0", "--port", "80"]
