from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Author, Book


class CatalogModelTests(TestCase):
    def test_author_string_representation(self):
        author = Author.objects.create(first_name="Karel", last_name="Capek")
        self.assertEqual(str(author), "Karel Capek")

    def test_book_invalid_isbn_raises_validation_error(self):
        book = Book(
            title="Invalid ISBN Book",
            isbn="not-an-isbn",
            publication_year=2000,
            language=Book.Language.CZECH,
        )
        with self.assertRaises(ValidationError):
            book.full_clean()
