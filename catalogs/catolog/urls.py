from django.urls import path, re_path
from. import views


urlpatterns = [
    path('', views.index, name='index'),
    path("books/" , views.BookListView.as_view(), name='books'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('books/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path("book/create/", views.BookCreateView.as_view(), name='book_create'),
    path("book/<int:pk>/update/" , views.BookUpdateView.as_view(), name='book_update'),
    path("book/<int:pk>/delete/" , views.BookDeleteView.as_view(), name='book_delete'),
    #re_path(r"^books/(?P<pk>\d+)$", views.BookDetailView.as_view(), name="book-detail"),
    re_path(r"^authors/(?P<pk>\d+)$" , views.AuthorDetailView.as_view(), name="author-detail"),
    path("authors/", views.AuthorListView.as_view(), name="authors"),
    path('author/create/', views.AuthorCreateView.as_view(), name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author_delete'),
    path("languages/", views.LanguageListView.as_view(), name="languages"),
    path("genres/", views.GenreListView.as_view(), name="genres"),
    path("genre/create/", views.GenreCreateView.as_view(), name="genre_create"),
    path("genre/<int:pk>/update/", views.GenreUpdateView.as_view() , name = "genre_update"),
    path("genre/<int:pk>/delete/" , views.GenreDeleteView.as_view() , name = "genre_delete"),
    path("bookstest/", views.getBooks , name="getBooks"),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('allborrowed/', views.BookBorrowedListView.as_view(), name='all-borrowed'),
    path("language/create", views.LanguageCreateView.as_view(), name="language_create"),
    path("language/<int:pk>/update/", views.LanguageUpdateView.as_view() , name= "language_update"),
    path("language/<int:pk>/delete/", views.LanguageDeleteView.as_view() , name= "language_delete"),
]
