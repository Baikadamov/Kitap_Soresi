from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('registeration/', registrationPage, name='registrationPage'),

    path('books/author/<slug:author_slug>', show_author, name='author'),
    path('books/', booksPage, name='booksPage'),
    path('books/genre/<slug:genre_slug>', show_genre, name='genre'),

    path('book/<slug:book_slug>', show_book, name='book'),
    path('cats/<int:catid>/', categories, name='cats'),  # http://127.0.0.1:8000/library/cats/
]
