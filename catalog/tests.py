from django.test import TestCase
from django.contrib.auth.models import Permission, User
from django.core.exceptions import ValidationError
from django.urls import reverse

from .models import Author, Book, Category


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


class CatalogViewTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(first_name="George", last_name="Orwell")
        self.category = Category.objects.create(name="Fiction")
        self.book = Book.objects.create(
            title="Nineteen Eighty-Four",
            isbn="9780451524935",
            publication_year=1949,
            language=Book.Language.ENGLISH,
            copies_total=3,
            is_available=True,
        )
        self.book.authors.add(self.author)
        self.book.categories.add(self.category)

    def test_book_list_page_loads(self):
        response = self.client.get(reverse("catalog:book_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Katalog knih")
        self.assertContains(response, self.book.title)

    def test_book_detail_page_loads(self):
        response = self.client.get(reverse("catalog:book_detail", kwargs={"slug": self.book.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.isbn)

    def test_book_list_search_filter(self):
        response = self.client.get(reverse("catalog:book_list"), {"q": "Orwell"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.title)

    def test_book_create_page_loads(self):
        response = self.client.get(reverse("catalog:book_create"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response.url)

    def test_book_create_requires_catalog_add_permission(self):
        user = User.objects.create_user(username="user-no-perm", password="StrongPass123!")
        self.client.login(username="user-no-perm", password="StrongPass123!")
        response = self.client.get(reverse("catalog:book_create"))
        self.assertEqual(response.status_code, 403)

    def test_book_create_allows_user_with_permission(self):
        user = User.objects.create_user(username="librarian1", password="StrongPass123!")
        permission = Permission.objects.get(codename="add_book")
        user.user_permissions.add(permission)
        self.client.login(username="librarian1", password="StrongPass123!")
        response = self.client.get(reverse("catalog:book_create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pridat knihu")
