from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.views import generic
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.urls import reverse_lazy
from catolog.models import Book, Author, BookInstance, Genre, Language
import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RenewBookForm

@login_required
def index(request):
    """View function for home page of site."""
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='d').count()
    num_authors = Author.objects.count()
    num_language = Language.objects.count()
    
    request.session.set_expiry(60)

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        "num_language": num_language,
        "num_visits" : num_visits,
    }

    return render(request, 'index.html', context=context)

@login_required
def getBooks( request, *args, **kwargs):
    
    books = Book.objects.all()
    return render(request, 'books/books.html', {'books': books})


@login_required
def getAuthores(request , *args , **kwargs):
    authors = Author.objects.all()
    return render(request, 'authors.html', {'authors': authors})

@login_required
def getGenres(request , *args, **kwargs):
    genres = Genre.objects.all()
    return render(request, 'genres.html', {'genres': genres})

@login_required
def getLanguages(request , *args, **kwargs):
    languages = Language.objects.all()
    return render(request, 'languages.html', {'languages': languages})



class BookListView( LoginRequiredMixin, generic.ListView):
    model = Book
    paginate_by = 3
    queryset = Book.objects.all()
    context_object_name = "books"
    template_name = "books/books.html"

class BookDetailView(LoginRequiredMixin,generic.DetailView):
    model = Book
    queryset = Book.objects.all()
    context_object_name = "book"
    template_name = "books/book_detail.html"



class BookCreateView(LoginRequiredMixin,generic.CreateView):
    model = Book
    template_name = "books/create.html"
    fields = "__all__"


class BookUpdateView(LoginRequiredMixin,generic.UpdateView):
    model = Book
    template_name = "books/create.html"
    fields = "__all__"



class BookDeleteView(LoginRequiredMixin,generic.DeleteView):
    model = Book
    success_url = reverse_lazy("books")
    template_name = "books/delete.html"


class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    paginate_by = 10
    queryset = Author.objects.all()
    context_object_name = "authors"
    template_name = "authors/authors.html"


class AuthorDetailView( LoginRequiredMixin,generic.DetailView):
    model = Author
    queryset = Author.objects.all()
    context_object_name = "author"
    template_name = "authors/author_detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context 

class AuthorCreateView(LoginRequiredMixin , generic.CreateView):
    model  = Author
    fields = "__all__"
    initial = {'date_of_death': '05/01/2018'}
    template_name = "authors/author_form.html"



class AuthorUpdateView(LoginRequiredMixin , generic.UpdateView):
    model = Author
    fields = ["name" , "date_of_death" , "date_of_birth"]
    template_name = "authors/author_form.html"



class AuthorDeleteView(LoginRequiredMixin , generic.DeleteView):
    model = Author
    success_url = reverse_lazy("authors")
    template_name = "authors/author_confirm_delete.html"



class LanguageListView(LoginRequiredMixin,generic.ListView):
    model = Language
    paginate_by = 10
    queryset = Language.objects.all()
    #queryset = Language.objects.filter(name__icontains="por")[:5]
    context_object_name = "languages"
    template_name = "languages/languages.html"
    
class BookBorrowedListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    queryset = BookInstance.objects.filter(status__exact='o').order_by('due_back')
    context_object_name = "borrowed_books"
    template_name = "catalog/all_borrowed.html"
    

class GenreListView(LoginRequiredMixin,generic.ListView):
    model = Genre
    queryset = Genre.objects.all()
    context_object_name = "genres"
    template_name = "genres/genres.html"

@login_required
def book_detail_view(request , primary_key):
    print("ola como estas : ", request.GET.get("pk"))
    book = get_object_or_404(Book, pk=primary_key)

    return render(request, 'catalog/book_detail.html', context={'book': book})


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
  
  

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            return HttpResponseRedirect(reverse('all-borrowed') )

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)
 