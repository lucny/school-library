# AGENTS.md — Django Školní knihovna

Tento soubor je pracovní manuál pro použití OpenCode agentů v tomto repozitáři.
Cíl: vybudovat výukový projekt postupně od základů až po nasazení, se smysluplným verzováním na GitHubu.

## Kde jsou agenti

- Projektoví agenti jsou v `.opencode/agents/`.
- Přehled a pořadí použití je v `.opencode/agents/README.md`.

## Pravidla spolupráce s agenty

- Postupuj po malých, ověřitelných krocích.
- Každá fáze musí mít: cíl, implementaci, ověření, dokumentační poznámku.
- Po dokončení fáze vytvoř commit + tag + krátké release notes.
- Pokud je zadání nejasné, nejdřív použij `@01-roadmap-coach`.

## Git strategie

- Hlavní větev: `main`.
- Pracovní větev: `feature/faze-X-kratky-popis`.
- Commit konvence:
  - `feat(scope): ...`
  - `fix(scope): ...`
  - `docs(scope): ...`
  - `refactor(scope): ...`
  - `test(scope): ...`
  - `chore(scope): ...`
- Tagy po fázích: `v0.1` až `v1.0`.

## 10fázový plán (roadmap)

### Fáze 1 — Inicializace projektu (tag `v0.1`)
- Agent: `@02-django-foundation`
- Cíl: vytvořit Django projekt, základní app strukturu, environment konfiguraci.
- Výstupy: funkční server, rozdělené settings, základní URL mapa.
- DoD: projekt běží lokálně bez chyb, základní README sekce „Spuštění“.

### Fáze 2 — Datový model katalogu (tag `v0.2`)
- Agent: `@04-library-domain`
- Cíl: modely pro knihy, autory, kategorie, přílohy.
- Výstupy: ORM vztahy, migrace, seed/demo data.
- DoD: migrace proběhnou čistě, data lze vložit a zobrazit v adminu.

### Fáze 3 — Views, routing, šablony, formuláře (tag `v0.3`)
- Agent: `@06-ui-templates-ajax`
- Cíl: CRUD a katalogové stránky přes Django views + template.
- Výstupy: seznam/detail knih, formuláře s validací, přehledné URL.
- DoD: základní uživatelský tok funguje end-to-end.

### Fáze 4 — Lokální autentizace a autorizace (tag `v0.4`)
- Agent: `@03-auth-oauth`
- Cíl: registrace, přihlášení, odhlášení, reset hesla, role.
- Výstupy: role čtenář/knihovník, ochrana vybraných endpointů.
- DoD: přístupová práva odpovídají roli uživatele.

### Fáze 5 — OAuth (Google, Microsoft, GitHub) (tag `v0.5`)
- Agent: `@03-auth-oauth`
- Cíl: přihlášení třetí stranou přes 3 providery.
- Výstupy: env konfigurace providerů, callback URL, bezpečnostní checklist.
- DoD: každý provider má úspěšný login flow v lokálním prostředí.

### Fáze 6 — Rezervace a výpůjčky (tag `v0.6`)
- Agent: `@05-circulation-and-reviews`
- Cíl: rezervace knih, správa stavu výpůjček a termínů.
- Výstupy: workflow rezervace/vrácení/prodlení, guardrails proti konfliktům.
- DoD: klíčové scénáře fungují a mají minimální testy.

### Fáze 7 — Hodnocení a recenze (tag `v0.7`)
- Agent: `@05-circulation-and-reviews`
- Cíl: jednoduché hodnocení knih a recenze čtenářů.
- Výstupy: model hodnocení (např. 1–5), recenze, moderace podle role.
- DoD: nelze porušit základní pravidla (duplicitní hodnocení, neoprávněné akce).

### Fáze 8 — Admin, i18n, static/media, AJAX (tag `v0.8`)
- Agent: `@07-admin-i18n-static`, `@06-ui-templates-ajax`
- Cíl: pokročilejší backend/UI praktiky pro výuku.
- Výstupy: admin customizace, cs/en mutace, static/media režimy, jednoduché AJAX prvky.
- DoD: admin je efektivní pro knihovníka, překlady a assets fungují stabilně.

### Fáze 9 — Docker a publikace (tag `v0.9`)
- Agent: `@08-release-docs-presenter`
- Cíl: kontejnerizace a reprodukovatelné spuštění.
- Výstupy: Dockerfile, docker-compose, deploy checklist.
- DoD: aplikace je spustitelná přes Docker jedním postupem.

### Fáze 10 — Dokumentace + prezentace (tag `v1.0`)
- Agent: `@08-release-docs-presenter`
- Cíl: finální výukový balíček.
- Výstupy: struktura Read the Docs, release notes, osnova prezentace s Nano Banana Pro.
- DoD: nový student zvládne projekt rozběhnout a chápe principy krok za krokem.

## Šablona release notes pro každou fázi

Použij při tagování:

- Co je nové
- Proč je to důležité
- Jak ověřit funkčnost
- Známá omezení
- Co následuje

## Rychlé prompty pro start

- `@01-roadmap-coach Připrav detailní plán pro Fáze 1–3 včetně checklistů a Definition of Done.`
- `@02-django-foundation Implementuj Fázi 1 jako malé commity s ověřením po každém kroku.`
- `@04-library-domain Navrhni modely pro Fázi 2 včetně migrací a demo seed dat.`
- `@03-auth-oauth Připrav Fáze 4–5 včetně bezpečnostního checklistu a env proměnných.`
- `@08-release-docs-presenter Připrav podklady pro Fáze 9–10 včetně RTD osnovy a release flow.`

## Konkrétní backlog — Fáze 1 (1–2h bloky)

### Blok 1 (1h) — Příprava repozitáře a větve
- Cíl: připravit čisté výchozí prostředí pro výukový vývoj.
- Úkoly:
  - vytvořit pracovní větev `feature/faze-1-inicializace`,
  - doplnit základní `.gitignore` pro Python/Django,
  - zapsat krátký cíl fáze do README (1 odstavec).
- Ověření:
  - `git status` neobsahuje neočekávané soubory,
  - větev je správně přepnutá.
- Commit:
  - `chore(repo): pripravena vyvojova vetev a zakladni ignorace`

### Blok 2 (1–2h) — Inicializace Django projektu
- Cíl: mít běžící minimální Django projekt.
- Úkoly:
  - vytvořit virtuální prostředí,
  - nainstalovat Django a inicializovat projekt,
  - vytvořit základní app `core` a napojit root URL.
- Ověření:
  - `python manage.py check` bez chyb,
  - `python manage.py runserver` a načtení výchozí stránky.
- Commit:
  - `feat(core): inicializace django projektu a app core`

### Blok 3 (1–2h) — Struktura aplikací knihovny
- Cíl: připravit logické členění projektu na domény.
- Úkoly:
  - vytvořit app: `accounts`, `catalog`, `circulation`, `reviews`,
  - zaregistrovat app v settings,
  - přidat základní URL namespace pro každou app.
- Ověření:
  - `python manage.py check` bez chyb,
  - root URL mapa obsahuje include pro všechny app.
- Commit:
  - `feat(apps): zalozeni domenovych django aplikaci`

### Blok 4 (1–2h) — Environment a settings split
- Cíl: oddělit konfigurační vrstvy pro dev/prod a tajné klíče.
- Úkoly:
  - rozdělit settings na `base.py`, `dev.py`, `prod.py`,
  - zavést `.env` a načítání proměnných,
  - nastavit `DEBUG`, `ALLOWED_HOSTS`, cesty pro static/media.
- Ověření:
  - server běží v dev režimu,
  - změna `.env` se projeví bez zásahu do kódu.
- Commit:
  - `refactor(settings): rozdeleni konfigurace a env promenne`

### Blok 5 (1h) — Základní stránka a healthcheck
- Cíl: mít minimální funkční UI základ a test běhu.
- Úkoly:
  - vytvořit jednoduchou homepage v `core`,
  - přidat `/health/` endpoint vracející 200,
  - přidat základní šablonu layoutu.
- Ověření:
  - homepage i `/health/` vrací očekávanou odpověď,
  - lokální běh bez tracebacku.
- Commit:
  - `feat(core): homepage a healthcheck endpoint`

### Blok 6 (1h) — README „Spuštění“ + ukončení fáze
- Cíl: dokončit Fázi 1 tak, aby ji zvládl nový student.
- Úkoly:
  - dopsat README sekci „Spuštění“ (Windows + obecný postup),
  - přidat stručný troubleshooting (2–3 nejčastější chyby),
  - připravit release notes pro `v0.1`.
- Ověření:
  - nový klon repa lze podle README rozběhnout,
  - fáze splňuje DoD z roadmapy.
- Commit:
  - `docs(readme): navod spusteni a release notes pro v0.1`

### Uzavření Fáze 1
- Sloučení větve do `main` po kontrole.
- Vytvoření tagu: `v0.1`.
- Vydání release notes podle šablony výše.

### Prompt pro okamžitý start
- `@02-django-foundation Realizuj Blok 1 a Blok 2 z AGENTS.md, po kazdem bloku proved overeni, navrhni commit message a cekej na potvrzeni pred dalsim blokem.`
