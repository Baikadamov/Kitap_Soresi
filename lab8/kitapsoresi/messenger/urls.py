from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('books/author/<slug:author_slug>', BooksAuthor.as_view(), name='author'),
    path('books/', BookHome.as_view(), name='booksPage'),
    path('books/genre/<slug:genre_slug>', BooksGenre.as_view(), name='genre'),

    path('addpage/', AddBook.as_view(), name='addbook'),

    path('book/<slug:book_slug>', ShowBook.as_view(), name='book'),

    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('profile/', profile, name='profile'),
    path('logout/', logout_user, name='logout'),
]
