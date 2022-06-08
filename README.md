# Сервис для выгрузки и анализа вакансий с hh ru api

## Стек

- `python3.10`
- `SQLAlchemy`
- `psycopg2`
- `requests`
- `pydantic`
- `alembic`

## Установка

### Настройка virtualenv

```Bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
test

### Настройка

В файле `settings.yaml.copy` лежит пример конфига сервиса.

- Секция `app`: настройки парсера (hh api url)
- Секция `postgres`: настройки базы данных (пользователь, пароль, бд, хост, порт)

### Запуск

```Bash
uvicorn app.service:app
```
