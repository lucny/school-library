from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from circulation.models import Loan, Reservation

from .constants import READER_GROUP
from .forms import SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:index")

    def form_valid(self, form):
        response = super().form_valid(form)
        reader_group, _ = Group.objects.get_or_create(name=READER_GROUP)
        self.object.groups.add(reader_group)
        login(self.request, self.object, backend="django.contrib.auth.backends.ModelBackend")
        return response


@login_required
def index(request):
    user = request.user

    active_loans = user.loans.select_related("book").filter(status=Loan.Status.ACTIVE).order_by("due_date")[:5]
    pending_reservations = (
        user.reservations.select_related("book").filter(status=Reservation.Status.PENDING).order_by("-reserved_at")[:5]
    )
    recent_reviews = user.reviews.select_related("book").order_by("-updated_at")[:5]

    context = {
        "active_loans": active_loans,
        "pending_reservations": pending_reservations,
        "recent_reviews": recent_reviews,
        "stats": {
            "ratings_count": user.ratings.count(),
            "reviews_count": user.reviews.count(),
            "active_loans_count": user.loans.filter(status=Loan.Status.ACTIVE).count(),
            "pending_reservations_count": user.reservations.filter(status=Reservation.Status.PENDING).count(),
        },
    }
    return render(request, "accounts/dashboard.html", context)
