from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from catalog.models import Book


class Rating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ratings")
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hodnocení"
        verbose_name_plural = "Hodnocení"
        ordering = ["-updated_at"]
        constraints = [models.UniqueConstraint(fields=["book", "user"], name="unique_rating_per_user_book")]
        indexes = [models.Index(fields=["score"], name="rating_score_idx")]

    def __str__(self):
        return f"{self.book.title} - {self.user} ({self.score})"


class Review(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Čeká na schválení"
        APPROVED = "approved", "Schválená"
        REJECTED = "rejected", "Zamítnutá"

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField(blank=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    moderation_note = models.CharField(max_length=255, blank=True)
    moderated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="moderated_reviews",
    )
    moderated_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Recenze"
        verbose_name_plural = "Recenze"
        ordering = ["-updated_at"]
        constraints = [models.UniqueConstraint(fields=["book", "user"], name="unique_review_per_user_book")]
        indexes = [models.Index(fields=["status"], name="review_status_idx")]

    def __str__(self):
        return f"{self.book.title} - {self.user} ({self.status})"
