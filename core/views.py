from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count
from django.shortcuts import render

from catalog.models import Author, Book
from circulation.models import Loan
from reviews.models import Review


def home(request):
    user_model = get_user_model()
    latest_books = Book.objects.prefetch_related("authors").order_by("-created_at")[:6]
    latest_reviews = Review.objects.select_related("book", "user").filter(status=Review.Status.APPROVED).order_by("-updated_at")[:5]
    top_books = (
        Book.objects.annotate(avg_rating=Avg("ratings__score"), ratings_count=Count("ratings"))
        .filter(ratings_count__gt=0)
        .order_by("-avg_rating", "-ratings_count", "title")[:3]
    )
    active_readers = user_model.objects.annotate(loans_total=Count("loans")).filter(loans_total__gt=0).order_by("-loans_total", "username")[:5]
    featured_book = (
        Book.objects.annotate(avg_rating=Avg("ratings__score"), ratings_count=Count("ratings"))
        .filter(ratings_count__gt=0)
        .order_by("-avg_rating", "-ratings_count", "title")
        .first()
    )
    if featured_book is None:
        featured_book = Book.objects.order_by("-created_at").first()
    author_of_week = Author.objects.annotate(book_count=Count("books")).filter(book_count__gt=0).order_by("-book_count", "last_name", "first_name").first()

    context = {
        "latest_books": latest_books,
        "latest_reviews": latest_reviews,
        "top_books": top_books,
        "active_readers": active_readers,
        "featured_book": featured_book,
        "author_of_week": author_of_week,
        "books_count": Book.objects.count(),
        "authors_count": Author.objects.count(),
        "reviews_count": Review.objects.filter(status=Review.Status.APPROVED).count(),
        "active_loans_count": Loan.objects.filter(status=Loan.Status.ACTIVE).count(),
    }
    return render(request, "core/home.html", context)


def health(request):
    return HttpResponse(b"ok", content_type="text/plain")


def permission_denied_view(request, exception):
    return render(request, "core/403.html", status=403)
