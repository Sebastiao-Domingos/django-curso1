from django.urls import path, re_path
from. import views


urlpatterns = [
    path('', views.index, name='index'),
    path("books/" , views.BookListView.as_view(), name='books'),
    #path('books/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    re_path(r"^books/(?P<pk>\d+)$", views.BookDetailView.as_view(), name="book-detail"),
    re_path(r"^authors/(?P<pk>\d+)$" , views.AuthorDetailView.as_view(), name="author-detail"),
    path("authors/", views.AuthorListView.as_view(), name="authors"),
    path("languages/", views.LanguageListView.as_view(), name="languages"),
    path("genres/", views.GenreListView.as_view(), name="genres"),
]
