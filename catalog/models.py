from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils.text import slugify


isbn_validator = RegexValidator(
    regex=r"^(?:97[89])?\d{9}[\dXx]$",
    message="ISBN must contain 10 or 13 digits (X allowed for ISBN-10 check digit).",
)


class Author(models.Model):
    first_name = models.CharField(max_length=120, verbose_name="First name")
    last_name = models.CharField(max_length=120, verbose_name="Last name")
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    biography = models.TextField(blank=True, verbose_name="Biography")
    portrait = models.ImageField(
        upload_to="authors/portraits/%Y/%m/",
        null=True,
        blank=True,
        verbose_name="Portrait",
    )
    birth_date = models.DateField(null=True, blank=True, verbose_name="Birth date")
    death_date = models.DateField(null=True, blank=True, verbose_name="Death date")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ["last_name", "first_name"]
        constraints = [
            models.UniqueConstraint(
                fields=["first_name", "last_name", "birth_date"],
                name="unique_author_identity",
            )
        ]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.first_name}-{self.last_name}")
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True, verbose_name="Name")
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Description")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Book(models.Model):
    class Language(models.TextChoices):
        CZECH = "cs", "Czech"
        ENGLISH = "en", "English"
        SLOVAK = "sk", "Slovak"
        GERMAN = "de", "German"
        OTHER = "other", "Other"

    title = models.CharField(max_length=255, verbose_name="Title")
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    subtitle = models.CharField(max_length=255, blank=True, verbose_name="Subtitle")
    isbn = models.CharField(
        max_length=13,
        unique=True,
        validators=[isbn_validator],
        verbose_name="ISBN",
        help_text="Enter ISBN-10 or ISBN-13 without separators.",
    )
    publication_year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1450), MaxValueValidator(date.today().year + 2)],
        verbose_name="Publication year",
    )
    language = models.CharField(
        max_length=10,
        choices=Language.choices,
        default=Language.CZECH,
        verbose_name="Language",
    )
    description = models.TextField(blank=True, verbose_name="Description")
    cover_image = models.ImageField(
        upload_to="books/covers/%Y/%m/",
        null=True,
        blank=True,
        verbose_name="Cover image",
    )
    authors = models.ManyToManyField(Author, related_name="books", verbose_name="Authors")
    categories = models.ManyToManyField(Category, related_name="books", blank=True, verbose_name="Categories")
    copies_total = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="Total copies",
    )
    is_available = models.BooleanField(default=True, verbose_name="Available")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ["title"]
        indexes = [
            models.Index(fields=["title"], name="book_title_idx"),
            models.Index(fields=["publication_year"], name="book_year_idx"),
            models.Index(fields=["is_available"], name="book_available_idx"),
        ]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class BookAttachment(models.Model):
    class AttachmentType(models.TextChoices):
        COVER = "cover", "Cover"
        SAMPLE_PDF = "sample_pdf", "Sample PDF"
        OTHER = "other", "Other"

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="attachments", verbose_name="Book")
    title = models.CharField(max_length=140, verbose_name="Title")
    attachment_type = models.CharField(
        max_length=20,
        choices=AttachmentType.choices,
        default=AttachmentType.OTHER,
        verbose_name="Attachment type",
    )
    file = models.FileField(upload_to="book_attachments/%Y/%m/", verbose_name="File")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Book attachment"
        verbose_name_plural = "Book attachments"
        ordering = ["-uploaded_at"]
        indexes = [models.Index(fields=["attachment_type"], name="book_attach_type_idx")]

    def __str__(self) -> str:
        return f"{self.book.title} - {self.title}"
