from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import BookForm, BookSearchForm
from .models import Book


class BookListView(ListView):
    model = Book
    template_name = "catalog/book_list.html"
    context_object_name = "books"
    paginate_by = 10

    def get_queryset(self):
        queryset = (
            Book.objects.select_related()
            .prefetch_related("authors", "categories")
            .order_by("title")
        )

        self.search_form = BookSearchForm(self.request.GET or None)
        if not self.search_form.is_valid():
            return queryset

        query = self.search_form.cleaned_data.get("q")
        category = self.search_form.cleaned_data.get("category")
        language = self.search_form.cleaned_data.get("language")
        available_only = self.search_form.cleaned_data.get("available_only")

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(subtitle__icontains=query)
                | Q(isbn__icontains=query)
                | Q(authors__first_name__icontains=query)
                | Q(authors__last_name__icontains=query)
            )
        if category:
            queryset = queryset.filter(categories=category)
        if language:
            queryset = queryset.filter(language=language)
        if available_only:
            queryset = queryset.filter(is_available=True)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = getattr(self, "search_form", BookSearchForm())
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = "catalog/book_detail.html"
    context_object_name = "book"
    slug_field = "slug"
    slug_url_kwarg = "slug"


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = "catalog/book_form.html"
    success_url = reverse_lazy("catalog:book_list")
