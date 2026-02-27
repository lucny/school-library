from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

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
    return render(request, "accounts/dashboard.html")
