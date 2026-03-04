from django import forms

from .models import Book, Category


class BookSearchForm(forms.Form):
    q = forms.CharField(required=False, label="Hledat")
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="Kategorie",
        empty_label="Všechny",
    )
    language = forms.ChoiceField(required=False, label="Jazyk")
    available_only = forms.BooleanField(required=False, label="Pouze dostupné")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        localized_language_choices = [("", "Všechny")] + [
            (Book.Language.CZECH, "Čeština"),
            (Book.Language.ENGLISH, "Angličtina"),
            (Book.Language.SLOVAK, "Slovenština"),
            (Book.Language.GERMAN, "Němčina"),
            (Book.Language.OTHER, "Jiný"),
        ]
        self.fields["language"].choices = localized_language_choices


class BookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].label = "Název"
        self.fields["subtitle"].label = "Podtitul"
        self.fields["publication_year"].label = "Rok vydání"
        self.fields["language"].label = "Jazyk"
        self.fields["language"].choices = [
            (Book.Language.CZECH, "Čeština"),
            (Book.Language.ENGLISH, "Angličtina"),
            (Book.Language.SLOVAK, "Slovenština"),
            (Book.Language.GERMAN, "Němčina"),
            (Book.Language.OTHER, "Jiný"),
        ]
        self.fields["description"].label = "Popis"
        self.fields["cover_image"].label = "Obálka"
        self.fields["authors"].label = "Autoři"
        self.fields["categories"].label = "Kategorie"
        self.fields["copies_total"].label = "Počet kusů"
        self.fields["is_available"].label = "Dostupná"
        self.fields["isbn"].help_text = "Zadejte ISBN-10 nebo ISBN-13 bez oddělovačů."

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
