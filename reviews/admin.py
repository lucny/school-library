from django.contrib import admin

from .models import Rating, Review


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("book", "user", "score", "updated_at")
    list_filter = ("score",)
    search_fields = ("book__title", "user__username", "user__email")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("book", "user", "status", "updated_at", "moderated_by")
    list_filter = ("status",)
    search_fields = ("book__title", "user__username", "user__email", "text")
