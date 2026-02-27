from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.db.models import Q
from django.dispatch import receiver

from .constants import LIBRARIAN_GROUP, READER_GROUP


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    Group.objects.get_or_create(name=READER_GROUP)
    librarian_group, _ = Group.objects.get_or_create(name=LIBRARIAN_GROUP)

    book_model = apps.get_model("catalog", "Book")
    reservation_model = apps.get_model("circulation", "Reservation")
    loan_model = apps.get_model("circulation", "Loan")
    permissions = Permission.objects.filter(
        Q(content_type__app_label="catalog", content_type__model=book_model._meta.model_name)
        | Q(content_type__app_label="circulation", content_type__model=reservation_model._meta.model_name)
        | Q(content_type__app_label="circulation", content_type__model=loan_model._meta.model_name)
    )
    librarian_group.permissions.add(*permissions)
