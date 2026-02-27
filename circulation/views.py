from django.shortcuts import render

from accounts.permissions import librarian_required
from .models import Loan, Reservation


@librarian_required
def index(request):
    active_loans = Loan.objects.select_related("book", "borrower").filter(status=Loan.Status.ACTIVE)[:20]
    pending_reservations = Reservation.objects.select_related("book", "requester").filter(status=Reservation.Status.PENDING)[
        :20
    ]
    context = {
        "active_loans": active_loans,
        "pending_reservations": pending_reservations,
    }
    return render(request, "circulation/dashboard.html", context)
