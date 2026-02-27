# Django — Školní knihovna

Tento repozitář slouží jako výukový projekt, ve kterém budeme krok po kroku stavět školní knihovnu v Django od inicializace projektu přes modely, autentizaci, rezervace a recenze až po Docker nasazení a dokumentaci.

## Spuštění

### Windows (PowerShell)

1. Vytvor virtualni prostredi:
   `python -m venv .venv`
2. Aktivuj virtualni prostredi:
   `.venv\Scripts\Activate.ps1`
3. Nainstaluj zavislosti:
   `python -m pip install -U pip`
   `python -m pip install Django python-dotenv`
4. Vytvor lokalni env soubor:
   `Copy-Item .env.example .env`
5. Spust migrace:
   `python manage.py migrate`
6. Spust server:
   `python manage.py runserver`

### Obecny postup (macOS/Linux)

1. `python3 -m venv .venv`
2. `source .venv/bin/activate`
3. `python -m pip install -U pip && python -m pip install Django python-dotenv`
4. `cp .env.example .env`
5. `python manage.py migrate`
6. `python manage.py runserver`

### Co je po Fazi 1 hotove

- Django projekt s modularni konfiguraci `config/settings/base.py`, `config/settings/dev.py`, `config/settings/prod.py`.
- Aplikace: `core`, `accounts`, `catalog`, `circulation`, `reviews`.
- Zakladni URL mapa pro vsechny aplikace.
- Uvodni homepage a endpoint `/health/`.

## Faze 2 - katalogovy model

- Modely: `Author`, `Category`, `Book`, `BookAttachment` v `catalog/models.py`.
- Admin registrace a zakladni konfigurace listu/filtru v `catalog/admin.py`.
- Seed demo data: `python manage.py seed_catalog`.

## Faze 3 - views, routovani, sablony, formulare

- Katalog ma stranky pro seznam knih, detail knihy a formular pro vlozeni nove knihy.
- Filtrovani v seznamu podporuje hledani, kategorii, jazyk a dostupnost.
- URL namespace:
  - `catalog:book_list`
  - `catalog:book_detail`
  - `catalog:book_create`

## Faze 4 - lokalni autentizace a role

- Registrace, prihlaseni, odhlaseni a reset hesla v app `accounts`.
- Pri registraci se uzivatel zaradi do role `reader`.
- Role `librarian` ma pristup ke sprave vypujcek (`circulation:index`).
- Vytvareni knih (`catalog:book_create`) je chraneno permission `catalog.add_book`.

### Troubleshooting

- Pokud nejde import `dotenv`, doinstaluj balicek `python-dotenv` do aktivniho virtualniho prostredi.
- Pokud `runserver` hlasi chybu se settings, over `DJANGO_SETTINGS_MODULE` (default je `config.settings.dev`).
- Pokud jsou problemy s migracemi, zkontroluj, ze mas vytvoreny `.env` podle `.env.example`.
