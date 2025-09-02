# Rick and Morty

### Requirements:
1. Endpoint, which returns a random character from the world of Rick and Morty series.
2. Endpoint gets `search_string` as an argument and returns a list of all characters, which contains the `search_string` in their names.
3. Regularly, the app downloads data from external service to inner DB.
4. Requests of implemented API should work with local DB (Take data from DB not from Rick & Morty API).

### Technologies to use:
1. Public API: https://rickandmortyapi.com/documentation.
2. Use Celery as a task scheduler for data synchronization for Rick & Morty API.
3. Python, Django/Flask/FastAPI, ORM, PostgreSQL, Git.
4. All endpoints should be documented via Swagger.

### How to run:
- Create virtual environment: `python -m venv venv`
- Activate virtual environment: `venv\Scripts\activate` on Windows, `source venv/bin/activate` on Linux or MacOS.
- Install dependencies: `pip install -r requirements.txt`
- Create a new Postgres DB and User
- Rename `env_sample` to `.env` and fill in the values
- Create superuser: `python manage.py createsuperuser`
- Run migrations: `python manage.py migrate`
- Run Redis server: `docker run -d -p 6379:6379 redis`
- Run Celery worker for tasks handling: `celery -A rick_and_morty_api worker -l INFO`
- Run Celery beat for tasks scheduling: `celery -A rick_and_morty beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler`
- Create a schedule for running sync in DB
- Run app in Django server: `python manage.py runserver`

