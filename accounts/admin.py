from django.contrib import admin
from django.apps import apps
from django.contrib.auth.admin import GroupAdmin as DjangoGroupAdmin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group

from .constants import LIBRARIAN_GROUP, READER_GROUP
from .models import SocialLink, User


ROLE_LABELS = {
    READER_GROUP: "Čtenář",
    LIBRARIAN_GROUP: "Knihovník",
}

PERMISSION_ACTION_LABELS = {
    "add": "Přidat",
    "change": "Upravit",
    "delete": "Smazat",
    "view": "Zobrazit",
}


def get_role_label(group_name):
    return ROLE_LABELS.get(group_name, group_name)


def get_permission_label(permission):
    action, separator, _ = permission.codename.partition("_")
    if action in PERMISSION_ACTION_LABELS and separator:
        model = permission.content_type.model_class()
        model_label = model._meta.verbose_name if model else permission.content_type.model
        try:
            app_config = apps.get_app_config(permission.content_type.app_label)
            app_label = app_config.verbose_name
        except LookupError:
            app_label = permission.content_type.app_label
        return f"{PERMISSION_ACTION_LABELS[action]} {model_label} — {app_label} ({permission.codename})"
    return f"{permission.name} ({permission.codename})"


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    fieldsets = DjangoUserAdmin.fieldsets + (("Profil", {"fields": ("profile_photo", "bio")}),)
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (("Profil", {"fields": ("profile_photo", "bio")}),)
    inlines = [SocialLinkInline]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        form_field = super().formfield_for_manytomany(db_field, request, **kwargs)
        if db_field.name == "groups" and form_field:
            form_field.label_from_instance = lambda group: f"{get_role_label(group.name)} ({group.name})"
        if db_field.name == "user_permissions" and form_field:
            form_field.label_from_instance = get_permission_label
        return form_field


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("user", "label", "url", "created_at")
    search_fields = ("user__username", "label", "url")


admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(DjangoGroupAdmin):
    list_display = ("name", "display_name")
    search_fields = ("name",)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        form_field = super().formfield_for_manytomany(db_field, request, **kwargs)
        if db_field.name == "permissions" and form_field:
            form_field.label_from_instance = get_permission_label
        return form_field

    @admin.display(description="Český název")
    def display_name(self, obj):
        return get_role_label(obj.name)
