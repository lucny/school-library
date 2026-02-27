from django.contrib import admin

from .models import Loan, Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("book", "requester", "status", "reserved_at", "expires_at")
    list_filter = ("status",)
    search_fields = ("book__title", "requester__username", "requester__email")


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ("book", "borrower", "status", "due_date", "borrowed_at", "returned_at")
    list_filter = ("status", "due_date")
    search_fields = ("book__title", "borrower__username", "borrower__email")
