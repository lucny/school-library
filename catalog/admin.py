from django.contrib import admin

from .models import Author, Book, BookAttachment, Category


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "birth_date", "death_date", "portrait")
    search_fields = ("first_name", "last_name")
    prepopulated_fields = {"slug": ("first_name", "last_name")}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class BookAttachmentInline(admin.TabularInline):
    model = BookAttachment
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "isbn", "publication_year", "language", "copies_total", "is_available", "cover_image")
    list_filter = ("language", "publication_year", "is_available", "categories")
    search_fields = ("title", "isbn", "authors__first_name", "authors__last_name")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("authors", "categories")
    inlines = [BookAttachmentInline]


@admin.register(BookAttachment)
class BookAttachmentAdmin(admin.ModelAdmin):
    list_display = ("title", "book", "attachment_type", "uploaded_at")
    list_filter = ("attachment_type",)
    search_fields = ("title", "book__title")
