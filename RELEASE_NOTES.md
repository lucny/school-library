# Release Notes

## v0.1
- Co je nove: inicializace projektu, app struktura, settings split, env, homepage, healthcheck.
- Proc je to dulezite: stabilni zaklad pro dalsi vyuku.
- Jak overit: `python manage.py check`, `python manage.py runserver`, `GET /health/`.
- Znama omezeni: bez domennich modelu a auth flow.
- Co nasleduje: modely katalogu.

## v0.2
- Co je nove: modely knih, autoru, kategorii a priloh, migrace, admin, seed.
- Proc je to dulezite: osvoji se ORM a datove vztahy.
- Jak overit: `python manage.py migrate`, `python manage.py seed_catalog`.
- Znama omezeni: chybi plne UI toky.
- Co nasleduje: views, sablony, formulare.

## v0.3
- Co je nove: katalog list/detail/create, filtrovani, URL namespace.
- Proc je to dulezite: prvni end-to-end tok v UI.
- Jak overit: `python manage.py test catalog`.
- Znama omezeni: zatim bez role-based auth.
- Co nasleduje: lokalni autentizace.

## v0.4
- Co je nove: registrace, login/logout, reset hesla, role reader/librarian.
- Proc je to dulezite: identita uzivatelu a autorizace endpointu.
- Jak overit: registrace + login + pristupy podle role.
- Znama omezeni: zatim bez social login.
- Co nasleduje: OAuth provideri.

## v0.5
- Co je nove: OAuth pres Google, Microsoft, GitHub (allauth).
- Proc je to dulezite: federovana autentizace v praxi.
- Jak overit: login flow pro kazdeho providera.
- Znama omezeni: vyzaduje provider app registrace a callback URL.
- Co nasleduje: rezervace a vypujcky.

## v0.6
- Co je nove: modely Reservation/Loan, stavy, guardrails, dashboard knihovnika.
- Proc je to dulezite: jadro knihovnickeho provozu.
- Jak overit: scenare rezervace-vypujcka-vraceni.
- Znama omezeni: zakladni workflow bez pokrocilych sankci.
- Co nasleduje: hodnoceni a recenze.

## v0.7
- Co je nove: rating 1-5, recenze, moderace.
- Proc je to dulezite: user-generated obsah a pravidla integrity.
- Jak overit: vlozeni hodnoceni + moderace roli librarian.
- Znama omezeni: bez anti-spam mechanik.
- Co nasleduje: i18n, admin, AJAX.

## v0.8
- Co je nove: i18n prepinani jazyka, admin branding, AJAX rezervace.
- Proc je to dulezite: pokrocilejsi UX a provozni detaily.
- Jak overit: zmena jazyka + rezervace bez reloadu.
- Znama omezeni: jen jednoduche AJAX interakce.
- Co nasleduje: Docker deploy.

## v0.9
- Co je nove: Dockerfile, docker-compose, PostgreSQL, entrypoint migrate/collectstatic.
- Proc je to dulezite: reprodukovatelne spusteni projektu.
- Jak overit: `docker compose up --build`.
- Znama omezeni: produkcni hardening je jen zaklad.
- Co nasleduje: RTD a prezentace.

## v1.0 (cil)
- Co je nove: kompletni RTD dokumentace, finalni release notes, prezentacni osnova.
- Proc je to dulezite: uzavreny vyukovy balicek pro nove studenty.
- Jak overit: student rozbehne projekt podle docs bez pomoci.
- Znama omezeni: dalsi rozsirovani uz mimo MVP scope.
- Co nasleduje: volitelne rozsireni (CI/CD, pokrocile testy, monitoring).
