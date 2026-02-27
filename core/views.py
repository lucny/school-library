from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, "core/home.html")


def health(request):
    return HttpResponse("ok", content_type="text/plain")


def permission_denied_view(request, exception):
    return render(request, "core/403.html", status=403)
