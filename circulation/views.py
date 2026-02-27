from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from accounts.permissions import librarian_required
from catalog.models import Book
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


@login_required
@require_POST
def reserve_book(request, slug):
    book = get_object_or_404(Book, slug=slug)
    active_loans = Loan.objects.filter(book=book, status=Loan.Status.ACTIVE).count()

    if active_loans < book.copies_total:
        return JsonResponse(
            {"ok": False, "message": "Kniha je momentalne dostupna. Rezervace neni potreba."},
            status=400,
        )

    reservation, created = Reservation.objects.get_or_create(
        book=book,
        requester=request.user,
        status=Reservation.Status.PENDING,
    )

    if created:
        return JsonResponse({"ok": True, "message": "Rezervace byla vytvorena."}, status=201)

    return JsonResponse({"ok": False, "message": "Uz mate aktivni rezervaci teto knihy."}, status=409)
