from django import forms

from .models import Rating, Review


class RatingReviewForm(forms.Form):
    score = forms.IntegerField(min_value=1, max_value=5, label="Hodnocení (1-5)")
    text = forms.CharField(required=False, widget=forms.Textarea, label="Recenze")


class ReviewModerationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].label = "Stav"
        self.fields["status"].choices = [
            (Review.Status.PENDING, "Čeká na schválení"),
            (Review.Status.APPROVED, "Schváleno"),
            (Review.Status.REJECTED, "Zamítnuto"),
        ]
        self.fields["moderation_note"].label = "Poznámka moderátora"

    class Meta:
        model = Review
        fields = ["status", "moderation_note"]


def save_rating_review(*, user, book, score, text):
    rating, _ = Rating.objects.update_or_create(book=book, user=user, defaults={"score": score})
    review, _ = Review.objects.update_or_create(
        book=book,
        user=user,
        defaults={"text": text, "status": Review.Status.PENDING, "moderation_note": "", "moderated_by": None, "moderated_at": None},
    )
    return rating, review
