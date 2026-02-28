import csv
from pathlib import Path
from datetime import date

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from catalog.models import Author, Book, Category


def parse_bool(value: str, default: bool = True) -> bool:
    if value is None:
        return default
    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "yes", "y", "ano"}:
        return True
    if normalized in {"0", "false", "no", "n", "ne"}:
        return False
    return default


def parse_date(value: str):
    if not value:
        return None
    raw = value.strip()
    if not raw:
        return None
    try:
        return date.fromisoformat(raw)
    except ValueError:
        return None


class Command(BaseCommand):
    help = "Import DB-agnostic seed data from CSV files in seed/."

    def add_arguments(self, parser):
        parser.add_argument("--path", default="seed", help="Path to seed directory (default: seed)")
        parser.add_argument(
            "--truncate",
            action="store_true",
            help="Delete catalog data before import (authors, books, categories)",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        root = Path(options["path"]).resolve()
        data_dir = root / "data"
        media_dir = root / "media"

        required = [
            data_dir / "authors.csv",
            data_dir / "books.csv",
            data_dir / "book_authors.csv",
            data_dir / "categories.csv",
            data_dir / "book_categories.csv",
        ]
        missing = [str(path) for path in required if not path.exists()]
        if missing:
            raise CommandError(f"Missing seed files: {', '.join(missing)}")

        if options["truncate"]:
            Book.objects.all().delete()
            Author.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.WARNING("Existing catalog data deleted."))

        categories_by_slug: dict[str, Category] = {}
        with (data_dir / "categories.csv").open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                slug = row["category_slug"].strip()
                if not slug:
                    continue
                category, _ = Category.objects.update_or_create(
                    slug=slug,
                    defaults={
                        "name": row.get("name", slug).strip() or slug,
                        "description": row.get("description", "").strip(),
                    },
                )
                categories_by_slug[slug] = category

        authors_by_slug: dict[str, Author] = {}
        with (data_dir / "authors.csv").open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                slug = row["author_slug"].strip()
                if not slug:
                    continue
                author, _ = Author.objects.update_or_create(
                    slug=slug,
                    defaults={
                        "first_name": row.get("first_name", "").strip(),
                        "last_name": row.get("last_name", "").strip(),
                        "biography": row.get("biography", "").strip(),
                        "birth_date": parse_date(row.get("birth_date", "")),
                        "death_date": parse_date(row.get("death_date", "")),
                    },
                )

                portrait = row.get("portrait", "").strip()
                if portrait:
                    portrait_path = media_dir / portrait
                    if portrait_path.exists():
                        with portrait_path.open("rb") as file_handle:
                            author.portrait.save(portrait_path.name, File(file_handle), save=True)

                authors_by_slug[slug] = author

        books_by_slug: dict[str, Book] = {}
        with (data_dir / "books.csv").open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                slug = row["book_slug"].strip()
                if not slug:
                    continue

                publication_year = int(row.get("publication_year") or 2000)
                copies_total = int(row.get("copies_total") or 1)
                is_available = parse_bool(row.get("is_available"), default=True)
                language = (row.get("language") or Book.Language.CZECH).strip() or Book.Language.CZECH
                if language not in {choice[0] for choice in Book.Language.choices}:
                    language = Book.Language.CZECH

                book, _ = Book.objects.update_or_create(
                    slug=slug,
                    defaults={
                        "title": row.get("title", "").strip(),
                        "subtitle": row.get("subtitle", "").strip(),
                        "isbn": row.get("isbn", "").strip(),
                        "publication_year": publication_year,
                        "language": language,
                        "description": row.get("description", "").strip(),
                        "copies_total": max(copies_total, 1),
                        "is_available": is_available,
                    },
                )

                cover = row.get("cover_image", "").strip()
                if cover:
                    cover_path = media_dir / cover
                    if cover_path.exists():
                        with cover_path.open("rb") as file_handle:
                            book.cover_image.save(cover_path.name, File(file_handle), save=True)

                books_by_slug[slug] = book

        with (data_dir / "book_authors.csv").open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                book_slug = row.get("book_slug", "").strip()
                author_slug = row.get("author_slug", "").strip()
                if not book_slug or not author_slug:
                    continue
                book = books_by_slug.get(book_slug)
                author = authors_by_slug.get(author_slug)
                if book and author:
                    book.authors.add(author)

        with (data_dir / "book_categories.csv").open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                book_slug = row.get("book_slug", "").strip()
                category_slug = row.get("category_slug", "").strip()
                if not book_slug or not category_slug:
                    continue
                book = books_by_slug.get(book_slug)
                category = categories_by_slug.get(category_slug)
                if book and category:
                    book.categories.add(category)

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed import complete: {len(authors_by_slug)} authors, {len(books_by_slug)} books, {len(categories_by_slug)} categories"
            )
        )
