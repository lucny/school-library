from django.test import TestCase
from django.contrib.auth.models import Group, User
from django.db import IntegrityError
from django.urls import reverse

from accounts.constants import LIBRARIAN_GROUP
from catalog.models import Book

from .models import Rating, Review


class ReviewsModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="reader-review", password="StrongPass123!")
        self.book = Book.objects.create(
            title="Reviewable Book",
            isbn="9788020000003",
            publication_year=2022,
        )

    def test_user_can_rate_book_only_once(self):
        Rating.objects.create(book=self.book, user=self.user, score=4)
        with self.assertRaises(IntegrityError):
            Rating.objects.create(book=self.book, user=self.user, score=5)

    def test_user_can_review_book_only_once(self):
        Review.objects.create(book=self.book, user=self.user, text="Prvni recenze")
        with self.assertRaises(IntegrityError):
            Review.objects.create(book=self.book, user=self.user, text="Druha recenze")


class ReviewsViewTests(TestCase):
    def setUp(self):
        self.reader = User.objects.create_user(username="reader-review2", password="StrongPass123!")
        self.librarian = User.objects.create_user(username="librarian-review", password="StrongPass123!")
        librarian_group = Group.objects.get(name=LIBRARIAN_GROUP)
        self.librarian.groups.add(librarian_group)
        self.book = Book.objects.create(
            title="Review UI Book",
            isbn="9788020000004",
            publication_year=2021,
        )

    def test_authenticated_user_can_submit_rating_and_review(self):
        self.client.login(username="reader-review2", password="StrongPass123!")
        response = self.client.post(
            reverse("reviews:add_for_book", kwargs={"slug": self.book.slug}),
            {"score": 5, "text": "Skvela kniha"},
        )
        self.assertRedirects(response, reverse("catalog:book_detail", kwargs={"slug": self.book.slug}))
        self.assertEqual(Rating.objects.get(book=self.book, user=self.reader).score, 5)
        review = Review.objects.get(book=self.book, user=self.reader)
        self.assertEqual(review.status, Review.Status.PENDING)

    def test_librarian_can_moderate_review(self):
        review = Review.objects.create(book=self.book, user=self.reader, text="Ke schvaleni")
        self.client.login(username="librarian-review", password="StrongPass123!")
        response = self.client.post(
            reverse("reviews:moderate", kwargs={"pk": review.pk}),
            {"status": Review.Status.APPROVED, "moderation_note": "OK"},
        )
        self.assertRedirects(response, reverse("reviews:index"))
        review.refresh_from_db()
        self.assertEqual(review.status, Review.Status.APPROVED)
        self.assertEqual(review.moderated_by, self.librarian)

    def test_reader_cannot_access_moderation(self):
        review = Review.objects.create(book=self.book, user=self.reader, text="Neopravnena moderace")
        self.client.login(username="reader-review2", password="StrongPass123!")
        response = self.client.get(reverse("reviews:moderate", kwargs={"pk": review.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response.url)
