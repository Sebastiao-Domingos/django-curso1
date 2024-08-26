from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import Http404
from django.views import generic
from django.shortcuts import get_object_or_404

from catolog.models import Book, Author, BookInstance, Genre, Language

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='d').count()
    num_authors = Author.objects.count()
    num_language = Language.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        "num_language": num_language
    }

    return render(request, 'index.html', context=context)


def getBooks( request, *args, **kwargs):
    books = Book.objects.all()
    return render(request, 'books.html', {'books': books})


def getAuthores(request , *args , **kwargs):
    authors = Author.objects.all()
    return render(request, 'authors.html', {'authors': authors})


def getGenres(request , *args, **kwargs):
    genres = Genre.objects.all()
    return render(request, 'genres.html', {'genres': genres})


def getLanguages(request , *args, **kwargs):
    languages = Language.objects.all()
    return render(request, 'languages.html', {'languages': languages})



class BookListView(generic.ListView):
    model = Book
    paginate_by = 3
    queryset = Book.objects.all()
    context_object_name = "books"
    template_name = "books/books.html"

class BookDetailView(generic.DetailView):
    model = Book
    queryset = Book.objects.all()
    context_object_name = "book"
    template_name = "books/book_detail.html"

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10
    queryset = Author.objects.all()
    context_object_name = "authors"
    template_name = "authors/authors.html"


class AuthorDetailView(generic.DetailView):
    model = Author
    queryset = Author.objects.all()
    context_object_name = "author"
    template_name = "authors/author_detail.html"

class LanguageListView(generic.ListView):
    model = Language
    paginate_by = 10
    queryset = Language.objects.all()
    #queryset = Language.objects.filter(name__icontains="por")[:5]
    context_object_name = "languages"
    template_name = "languages/languages.html"


    #def get_queryset(self) -> QuerySet[Any]:
       # return Language.objects.filter(name__icontains="f")[:5]
    


class GenreListView(generic.ListView):
    model = Genre
    queryset = Genre.objects.all()
    context_object_name = "genres"
    template_name = "genres/genres.html"


def book_detail_view(request , primary_key):
    print("ola como estas : ", request.GET.get("pk"))
    book = get_object_or_404(Book, pk=primary_key)

    return render(request, 'catalog/book_detail.html', context={'book': book})
