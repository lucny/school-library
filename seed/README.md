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

Volitelně vymazání katalogových dat před importem:

```bash
python manage.py import_seed --path seed --truncate
```

## Poznámky

- Vazby používají stabilní slug klíče, nikoliv databázová ID.
- `books.csv` obsahuje technicky validní unikátní ISBN hodnoty pro importní účely.
- Pole `cover_image` a `portrait` jsou připravená pro relativní cesty vůči `seed/media`.
