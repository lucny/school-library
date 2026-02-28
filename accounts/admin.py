from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import SocialLink, User


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    fieldsets = DjangoUserAdmin.fieldsets + (("Profile", {"fields": ("profile_photo", "bio")}),)
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (("Profile", {"fields": ("profile_photo", "bio")}),)
    inlines = [SocialLinkInline]


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("user", "label", "url", "created_at")
    search_fields = ("user__username", "label", "url")
