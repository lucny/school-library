# Seed dataset: maturitni seznam 2025/2026

Tato složka obsahuje DB-agnostický seed balík pro import přes Django ORM.

## Struktura

- `data/authors.csv`
- `data/books.csv`
- `data/book_authors.csv`
- `data/categories.csv`
- `data/book_categories.csv`
- `media/authors/portraits/`
- `media/books/covers/`
- `media/users/profile_photos/`

## Import

```bash
python manage.py import_seed --path seed
```

## Provozní demo data (uživatelé, výpůjčky, rezervace, hodnocení, recenze)

Pro rychlé naplnění aplikace daty pro běžné testování provozu:

```bash
python manage.py seed_operational_data
```

Výchozí hodnoty commandu:

- 3 knihovníci (`librarian01` až `librarian03`)
- 15 čtenářů (`reader01` až `reader15`)
- 100 hodnocení
- 70 recenzí
- 25 aktivních výpůjček
- 35 vrácených výpůjček
- 20 čekajících rezervací
- heslo nových účtů: `TestPass123!`

Možnosti přizpůsobení:

```bash
python manage.py seed_operational_data --librarians 3 --readers 20 --active-loans 40 --returned-loans 60 --pending-reservations 30 --ratings 150 --reviews 120 --password "MojeSilneHeslo123!"
```

### Reset provozních demo dat

Bezpečný náhled, co by se mazalo:

```bash
python manage.py reset_operational_data --dry-run
```

Skutečné smazání uživatelů z provozního seedu (`reader*`, `librarian*`) a navázaných dat:

```bash
python manage.py reset_operational_data
```

Volitelně i smazání automaticky generovaných knih:

```bash
python manage.py reset_operational_data --remove-generated-books
```

Volitelně vymazání katalogových dat před importem:

```bash
python manage.py import_seed --path seed --truncate
```

## Poznámky

- Vazby používají stabilní slug klíče, nikoliv databázová ID.
- `books.csv` obsahuje technicky validní unikátní ISBN hodnoty pro importní účely.
- Pole `cover_image` a `portrait` jsou připravená pro relativní cesty vůči `seed/media`.
