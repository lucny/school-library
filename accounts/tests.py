from django.test import TestCase
from django.contrib.auth.models import Group, User
from django.urls import reverse

from .constants import LIBRARIAN_GROUP, READER_GROUP


class AccountsFlowTests(TestCase):
    def test_signup_creates_and_logs_in_user(self):
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "username": "student1",
                "email": "student@example.com",
                "first_name": "Eva",
                "last_name": "Novakova",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )
        self.assertRedirects(response, reverse("accounts:index"))
        self.assertTrue(User.objects.filter(username="student1").exists())

    def test_login_page_loads(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Prihlaseni")


class RolesTests(TestCase):
    def test_groups_created_after_migrate(self):
        self.assertTrue(Group.objects.filter(name=READER_GROUP).exists())
        self.assertTrue(Group.objects.filter(name=LIBRARIAN_GROUP).exists())

# Create your tests here.
