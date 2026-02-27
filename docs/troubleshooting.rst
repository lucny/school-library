Troubleshooting
===============

Server nenabehne
----------------
- Over aktivni virtualni prostredi.
- Over ``DJANGO_SETTINGS_MODULE`` (default ``config.settings.dev``).
- Spust ``python manage.py check``.

Problemy s OAuth
----------------
- Zkontroluj ``GOOGLE_*``, ``MICROSOFT_*``, ``GITHUB_*`` v ``.env``.
- Over callback URL v provider konzoli.
- Over, ze URL jsou pod ``/accounts/oauth/``.

Problemy s Dockerem
-------------------
- Over, ze existuje ``.env``.
- Projdi konfiguraci: ``docker compose config``.
- Pokud je problem s DB, zkontroluj hodnoty ``POSTGRES_*``.

Problemy s opravneni
--------------------
- Over role uzivatele (``reader`` nebo ``librarian``).
- Pro povyseni pouzij: ``python manage.py assign_librarian <username>``.
