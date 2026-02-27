from django.shortcuts import render

from accounts.permissions import librarian_required


@librarian_required
def index(request):
    return render(request, "circulation/dashboard.html")
