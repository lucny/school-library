from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.urls import reverse

from .constants import LIBRARIAN_GROUP, READER_GROUP

User = get_user_model()


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
        self.assertTrue(User.objects.get(username="student1").groups.filter(name=READER_GROUP).exists())

    def test_login_page_loads(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Prihlaseni")

    def test_login_page_shows_oauth_options(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertContains(response, "OAuth prihlaseni")
        self.assertContains(response, "Google")
        self.assertContains(response, "Microsoft")
        self.assertContains(response, "GitHub")


class RolesTests(TestCase):
    def test_groups_created_after_migrate(self):
        self.assertTrue(Group.objects.filter(name=READER_GROUP).exists())
        self.assertTrue(Group.objects.filter(name=LIBRARIAN_GROUP).exists())

    def test_assign_librarian_command(self):
        user = User.objects.create_user(username="test-reader", password="StrongPass123!")
        call_command("assign_librarian", user.username)
        user.refresh_from_db()
        self.assertTrue(user.groups.filter(name=LIBRARIAN_GROUP).exists())
