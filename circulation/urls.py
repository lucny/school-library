from django.urls import path

from . import views

app_name = "circulation"

urlpatterns = [
    path("", views.index, name="index"),
]
