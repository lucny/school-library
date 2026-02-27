from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand, CommandError

from accounts.constants import LIBRARIAN_GROUP


class Command(BaseCommand):
    help = "Assign librarian role to an existing user."

    def add_arguments(self, parser):
        parser.add_argument("username", type=str, help="Username to promote to librarian")

    def handle(self, *args, **options):
        username = options["username"]
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist as exc:
            raise CommandError(f"User '{username}' does not exist.") from exc

        group, _ = Group.objects.get_or_create(name=LIBRARIAN_GROUP)
        user.groups.add(group)
        self.stdout.write(self.style.SUCCESS(f"User '{username}' is now librarian."))
