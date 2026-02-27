from django.urls import path

from . import views

app_name = "reviews"

urlpatterns = [
    path("", views.index, name="index"),
    path("book/<slug:slug>/add/", views.add_for_book, name="add_for_book"),
    path("<int:pk>/moderate/", views.moderate, name="moderate"),
]
