# Test service for uploading vacancies from api.hh.ru
A small project work for the university.<br>
The service collects data on vacancies of backend developers in Russia, then aggregates and returns the data for the frontend.<br>
The project was created to analyze the demand for backend developers in Russia.<br>

## Technology

- `python3.10`
- `SQLAlchemy`
- `psycopg2`
- `requests`
- `pydantic`
- `alembic`

## Config

Copy the `settings.yaml.copy` file to `settings.yaml`

- Section `app`:
- - `cache_folder` - Cache folder for parselib
- Section `postgres`:
- - `user` - Database user
- - `password` - Database password
- - `database` - Database name
- - `host` -  Postgres host
- - `port` -  Postgres port
