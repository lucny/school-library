from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.BookListView.as_view(), name="book_list"),
    path("new/", views.BookCreateView.as_view(), name="book_create"),
    path("<slug:slug>/", views.BookDetailView.as_view(), name="book_detail"),
]
