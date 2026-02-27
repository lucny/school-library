Spusteni projektu
=================

Lokalni beh (Python)
--------------------

1. Vytvor virtualni prostredi: ``python -m venv .venv``
2. Aktivuj virtualni prostredi.
3. Nainstaluj zavislosti: ``python -m pip install -r requirements.txt``
4. Vytvor ``.env`` z ``.env.example``.
5. Proved migrace: ``python manage.py migrate``
6. Spust server: ``python manage.py runserver``

Lokalni beh (Docker)
--------------------

1. Vytvor ``.env`` z ``.env.example``.
2. Spust stack: ``docker compose up --build``
3. Otevri aplikaci: ``http://127.0.0.1:8000/``

Rychle ovreni
-------------

- ``python manage.py check``
- ``python manage.py test``
- ``/health/`` vraci HTTP 200
