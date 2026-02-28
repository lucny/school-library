from django import forms

from .models import Book, Category


class BookSearchForm(forms.Form):
    q = forms.CharField(required=False, label="Hledat")
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="Kategorie",
        empty_label="Vsechny",
    )
    language = forms.ChoiceField(required=False, label="Jazyk")
    available_only = forms.BooleanField(required=False, label="Pouze dostupne")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["language"].choices = [("", "Vsechny")] + list(Book.Language.choices)


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            "title",
            "subtitle",
            "isbn",
            "publication_year",
            "language",
            "description",
            "cover_image",
            "authors",
            "categories",
            "copies_total",
            "is_available",
        ]
