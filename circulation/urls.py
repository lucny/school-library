from django.urls import path

from . import views

app_name = "circulation"

urlpatterns = [
    path("", views.index, name="index"),
    path("reserve/<slug:slug>/", views.reserve_book, name="reserve_book"),
]
