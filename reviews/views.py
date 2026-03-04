from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.permissions import librarian_required
from catalog.models import Book

from .forms import RatingReviewForm, ReviewModerationForm, save_rating_review
from .models import Review


def index(request):
    approved_reviews = Review.objects.select_related("book", "user").filter(status=Review.Status.APPROVED)[:30]
    is_librarian = request.user.is_authenticated and request.user.groups.filter(name="librarian").exists()
    pending_reviews = []
    if is_librarian:
        pending_reviews = Review.objects.select_related("book", "user").filter(status=Review.Status.PENDING)[:30]
    return render(
        request,
        "reviews/index.html",
        {"approved_reviews": approved_reviews, "pending_reviews": pending_reviews, "is_librarian": is_librarian},
    )


def add_for_book(request, slug):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    book = get_object_or_404(Book, slug=slug)
    initial = {}

    existing_rating = request.user.ratings.filter(book=book).first()
    if existing_rating:
        initial["score"] = existing_rating.score
    existing_review = request.user.reviews.filter(book=book).first()
    if existing_review:
        initial["text"] = existing_review.text

    form = RatingReviewForm(request.POST or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        save_rating_review(
            user=request.user,
            book=book,
            score=form.cleaned_data["score"],
            text=form.cleaned_data["text"],
        )
        messages.success(request, "Hodnocení a recenze byly uloženy.")
        return redirect("catalog:book_detail", slug=book.slug)

    return render(request, "reviews/review_form.html", {"book": book, "form": form})


@librarian_required
def moderate(request, pk):
    review = get_object_or_404(Review.objects.select_related("book", "user"), pk=pk)
    form = ReviewModerationForm(request.POST or None, instance=review)
    if request.method == "POST" and form.is_valid():
        moderated_review = form.save(commit=False)
        moderated_review.moderated_by = request.user
        moderated_review.moderated_at = timezone.now()
        moderated_review.save()
        messages.success(request, "Moderace recenze byla uložena.")
        return redirect("reviews:index")
    return render(request, "reviews/moderate_review.html", {"review": review, "form": form})
