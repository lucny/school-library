from django.test import TestCase
from django.contrib.auth.models import Group, User
from django.urls import reverse

from accounts.constants import LIBRARIAN_GROUP


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

# Create your tests here.
