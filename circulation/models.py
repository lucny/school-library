from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from catalog.models import Book


def default_due_date():
    return timezone.localdate() + timedelta(days=14)


class Reservation(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Čekající"
        FULFILLED = "fulfilled", "Vyřízená"
        CANCELLED = "cancelled", "Zrušená"
        EXPIRED = "expired", "Expirovaná"

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reservations")
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservations")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    reserved_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Rezervace"
        verbose_name_plural = "Rezervace"
        ordering = ["-reserved_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["book", "requester"],
                condition=models.Q(status="pending"),
                name="unique_pending_reservation_per_user_book",
            )
        ]
        indexes = [models.Index(fields=["status"], name="reservation_status_idx")]

    def __str__(self):
        return f"Reservation: {self.book} - {self.requester}"

    def save(self, *args, **kwargs):
        if self.status == self.Status.PENDING and self.expires_at is None:
            self.expires_at = timezone.now() + timedelta(days=7)
        super().save(*args, **kwargs)


class Loan(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Aktivní"
        RETURNED = "returned", "Vrácená"
        OVERDUE = "overdue", "Po termínu"

    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name="loans")
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="loans")
    handled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="processed_loans",
    )
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(default=default_due_date)
    returned_at = models.DateTimeField(null=True, blank=True)
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Výpůjčka"
        verbose_name_plural = "Výpůjčky"
        ordering = ["-borrowed_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["book", "borrower"],
                condition=models.Q(status="active"),
                name="unique_active_loan_per_user_book",
            )
        ]
        indexes = [
            models.Index(fields=["status"], name="loan_status_idx"),
            models.Index(fields=["due_date"], name="loan_due_date_idx"),
        ]

    def __str__(self):
        return f"Loan: {self.book} - {self.borrower}"

    def clean(self):
        super().clean()
        if self.due_date and self.borrowed_at and self.due_date < self.borrowed_at.date():
            raise ValidationError({"due_date": "Datum vrácení nemůže být dříve než datum vypůjčení."})

        if self.status == self.Status.ACTIVE:
            active_loans_count = Loan.objects.filter(book=self.book, status=self.Status.ACTIVE).exclude(pk=self.pk).count()
            if active_loans_count >= self.book.copies_total:
                raise ValidationError("Pro tuto knihu není aktuálně dostupný žádný výtisk.")

        if self.status == self.Status.RETURNED and self.returned_at is None:
            raise ValidationError({"returned_at": "Vrácená výpůjčka musí mít vyplněný čas vrácení."})

    def save(self, *args, **kwargs):
        if self.returned_at and self.status != self.Status.RETURNED:
            self.status = self.Status.RETURNED
        self.full_clean()
        super().save(*args, **kwargs)

    def mark_returned(self):
        self.returned_at = timezone.now()
        self.status = self.Status.RETURNED
        self.save(update_fields=["returned_at", "status"])

    @property
    def is_overdue(self):
        return self.status == self.Status.ACTIVE and self.due_date < timezone.localdate()
