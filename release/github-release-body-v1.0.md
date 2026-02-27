## Co je nove
- Dokoncen vyukovy projekt "Django - Skolni knihovna" od inicializace az po Docker deploy.
- Implementovany katalog knih (autori, kategorie, prilohy), role-based autentizace a OAuth (Google, Microsoft, GitHub).
- Doplneny rezervace a vypujcky, hodnoceni a recenze s moderaci, i18n prepinani jazyka a AJAX rezervace bez reloadu.
- Pripravena dokumentace pro Read the Docs (Sphinx) a osnova prezentace vcetne promptu pro Nano Banana Pro.

## Proc je to dulezite
- Projekt slouzi jako kompletni studijni sada pro Django vyuku v logickych fazich v0.1-v1.0.
- Studenti vidi realisticky vyvoj aplikace: modely, views, auth, domennou logiku, testy i nasazeni.

## Jak overit funkcnost
1. Lokalni beh:
   - `python -m venv .venv`
   - `.venv\\Scripts\\python.exe -m pip install -r requirements.txt`
   - `Copy-Item .env.example .env`
   - `.venv\\Scripts\\python.exe manage.py migrate`
   - `.venv\\Scripts\\python.exe manage.py test`
   - `.venv\\Scripts\\python.exe manage.py runserver`
2. Docker beh:
   - `docker compose up --build`
   - otevrit `http://127.0.0.1:8000/`
3. Dokumentace:
   - `.venv\\Scripts\\python.exe -m pip install -r docs/requirements.txt`
   - `.venv\\Scripts\\python.exe -m sphinx -b html docs docs/_build/html`
   - otevrit `docs/_build/html/index.html`

## Znama omezeni
- OAuth vyzaduje rucni registraci aplikaci u provideru a spravne callback URL.
- Frontend je zamerne jednoduchy (Django templates + lehky AJAX) kvuli vyukovemu scope.
- Produkcni hardening je zakladni; doporuceno doplnit CI/CD, monitoring a bezpecnostni audit.

## Co nasleduje
- Volitelne navazujici rozsireni: API vrstva (DRF), pokrocile testy, CI pipeline, observability.
