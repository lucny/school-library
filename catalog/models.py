from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils.text import slugify


isbn_validator = RegexValidator(
    regex=r"^(?:97[89])?\d{9}[\dXx]$",
    message="ISBN musí obsahovat 10 nebo 13 znaků (u ISBN-10 je povoleno X jako kontrolní znak).",
)


class Author(models.Model):
    first_name = models.CharField(max_length=120, verbose_name="Jméno")
    last_name = models.CharField(max_length=120, verbose_name="Příjmení")
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    biography = models.TextField(blank=True, verbose_name="Biografie")
    portrait = models.ImageField(
        upload_to="authors/portraits/%Y/%m/",
        null=True,
        blank=True,
        verbose_name="Portrét",
    )
    birth_date = models.DateField(null=True, blank=True, verbose_name="Datum narození")
    death_date = models.DateField(null=True, blank=True, verbose_name="Datum úmrtí")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autoři"
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
    name = models.CharField(max_length=120, unique=True, verbose_name="Název")
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Popis")

    class Meta:
        verbose_name = "Kategorie"
        verbose_name_plural = "Kategorie"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Book(models.Model):
    class Language(models.TextChoices):
        CZECH = "cs", "Čeština"
        ENGLISH = "en", "Angličtina"
        SLOVAK = "sk", "Slovenština"
        GERMAN = "de", "Němčina"
        OTHER = "other", "Jiný"

    title = models.CharField(max_length=255, verbose_name="Název")
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    subtitle = models.CharField(max_length=255, blank=True, verbose_name="Podtitul")
    isbn = models.CharField(
        max_length=13,
        unique=True,
        validators=[isbn_validator],
        verbose_name="ISBN",
        help_text="Zadejte ISBN-10 nebo ISBN-13 bez oddělovačů.",
    )
    publication_year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1450), MaxValueValidator(date.today().year + 2)],
        verbose_name="Rok vydání",
    )
    language = models.CharField(
        max_length=10,
        choices=Language.choices,
        default=Language.CZECH,
        verbose_name="Jazyk",
    )
    description = models.TextField(blank=True, verbose_name="Popis")
    cover_image = models.ImageField(
        upload_to="books/covers/%Y/%m/",
        null=True,
        blank=True,
        verbose_name="Obálka",
    )
    authors = models.ManyToManyField(Author, related_name="books", verbose_name="Autoři")
    categories = models.ManyToManyField(Category, related_name="books", blank=True, verbose_name="Kategorie")
    copies_total = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="Počet kusů",
    )
    is_available = models.BooleanField(default=True, verbose_name="Dostupná")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Kniha"
        verbose_name_plural = "Knihy"
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
        COVER = "cover", "Obálka"
        SAMPLE_PDF = "sample_pdf", "Ukázkové PDF"
        OTHER = "other", "Jiné"

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="attachments", verbose_name="Kniha")
    title = models.CharField(max_length=140, verbose_name="Název")
    attachment_type = models.CharField(
        max_length=20,
        choices=AttachmentType.choices,
        default=AttachmentType.OTHER,
        verbose_name="Typ přílohy",
    )
    file = models.FileField(upload_to="book_attachments/%Y/%m/", verbose_name="Soubor")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Příloha knihy"
        verbose_name_plural = "Přílohy knih"
        ordering = ["-uploaded_at"]
        indexes = [models.Index(fields=["attachment_type"], name="book_attach_type_idx")]

    def __str__(self) -> str:
        return f"{self.book.title} - {self.title}"
