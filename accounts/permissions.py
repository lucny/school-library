from django.contrib.auth.decorators import user_passes_test

from .constants import LIBRARIAN_GROUP


def librarian_required(view_func):
    return user_passes_test(
        lambda user: user.is_authenticated and user.groups.filter(name=LIBRARIAN_GROUP).exists()
    )(view_func)
