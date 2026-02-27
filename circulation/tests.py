from datetime import timedelta

from django.test import TestCase
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.urls import reverse

from accounts.constants import LIBRARIAN_GROUP
from catalog.models import Book

from .models import Loan, Reservation


class CirculationAccessTests(TestCase):
    def setUp(self):
        self.reader = User.objects.create_user(username="reader", password="StrongPass123!")
        self.librarian = User.objects.create_user(username="librarian", password="StrongPass123!")
        librarian_group = Group.objects.get(name=LIBRARIAN_GROUP)
        self.librarian.groups.add(librarian_group)

    def test_anonymous_user_redirected_to_login(self):
        response = self.client.get(reverse("circulation:index"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response.url)

    def test_reader_cannot_access_librarian_dashboard(self):
        self.client.login(username="reader", password="StrongPass123!")
        response = self.client.get(reverse("circulation:index"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response.url)

    def test_librarian_can_access_dashboard(self):
        self.client.login(username="librarian", password="StrongPass123!")
        response = self.client.get(reverse("circulation:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sprava vypujcek")


class CirculationModelTests(TestCase):
    def setUp(self):
        self.reader = User.objects.create_user(username="reader2", password="StrongPass123!")
        self.other_reader = User.objects.create_user(username="reader3", password="StrongPass123!")
        self.librarian = User.objects.create_user(username="librarian2", password="StrongPass123!")
        self.book = Book.objects.create(
            title="Model Testing Book",
            isbn="9788020000002",
            publication_year=2020,
            copies_total=1,
            is_available=True,
        )

    def test_unique_pending_reservation_per_user_book(self):
        Reservation.objects.create(book=self.book, requester=self.reader)
        with self.assertRaises(ValidationError):
            reservation = Reservation(book=self.book, requester=self.reader, status=Reservation.Status.PENDING)
            reservation.full_clean()

    def test_loan_cannot_exceed_available_copies(self):
        Loan.objects.create(book=self.book, borrower=self.reader, handled_by=self.librarian)
        with self.assertRaises(ValidationError):
            Loan.objects.create(book=self.book, borrower=self.other_reader, handled_by=self.librarian)

    def test_loan_can_be_marked_returned(self):
        loan = Loan.objects.create(book=self.book, borrower=self.reader, handled_by=self.librarian)
        loan.mark_returned()
        loan.refresh_from_db()
        self.assertEqual(loan.status, Loan.Status.RETURNED)
        self.assertIsNotNone(loan.returned_at)

    def test_active_loan_overdue_property(self):
        loan = Loan.objects.create(
            book=self.book,
            borrower=self.reader,
            handled_by=self.librarian,
            due_date=timezone.localdate() - timedelta(days=1),
        )
        self.assertTrue(loan.is_overdue)
