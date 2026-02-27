from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .constants import LIBRARIAN_GROUP, READER_GROUP


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    if sender.name != "accounts":
        return

    Group.objects.get_or_create(name=READER_GROUP)
    librarian_group, _ = Group.objects.get_or_create(name=LIBRARIAN_GROUP)

    book_model = apps.get_model("catalog", "Book")
    permissions = Permission.objects.filter(content_type__app_label="catalog", content_type__model=book_model._meta.model_name)
    librarian_group.permissions.add(*permissions)
