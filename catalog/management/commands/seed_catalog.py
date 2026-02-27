from django.core.management.base import BaseCommand

from catalog.models import Author, Book, Category


class Command(BaseCommand):
    help = "Seed demo catalog data for local development."

    def handle(self, *args, **options):
        fiction, _ = Category.objects.get_or_create(name="Fiction")
        science, _ = Category.objects.get_or_create(name="Science")
        history, _ = Category.objects.get_or_create(name="History")

        capek, _ = Author.objects.get_or_create(first_name="Karel", last_name="Capek")
        orwell, _ = Author.objects.get_or_create(first_name="George", last_name="Orwell")
        hawking, _ = Author.objects.get_or_create(first_name="Stephen", last_name="Hawking")

        books = [
            {
                "title": "R.U.R.",
                "isbn": "9788020000001",
                "publication_year": 1920,
                "language": Book.Language.CZECH,
                "authors": [capek],
                "categories": [fiction],
            },
            {
                "title": "Nineteen Eighty-Four",
                "isbn": "9780451524935",
                "publication_year": 1949,
                "language": Book.Language.ENGLISH,
                "authors": [orwell],
                "categories": [fiction],
            },
            {
                "title": "A Brief History of Time",
                "isbn": "9780553380163",
                "publication_year": 1988,
                "language": Book.Language.ENGLISH,
                "authors": [hawking],
                "categories": [science, history],
            },
        ]

        created = 0
        for item in books:
            book, is_created = Book.objects.get_or_create(
                isbn=item["isbn"],
                defaults={
                    "title": item["title"],
                    "publication_year": item["publication_year"],
                    "language": item["language"],
                },
            )
            book.authors.set(item["authors"])
            book.categories.set(item["categories"])
            if is_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Catalog seed completed. New books: {created}"))
