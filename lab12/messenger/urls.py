from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', index, name='home'),
    path('books/author/<slug:author_slug>', BooksAuthor.as_view(), name='author'),
    path('books/', BookHome.as_view(), name='booksPage'),
    path('books/genre/<slug:genre_slug>', BooksGenre.as_view(), name='genre'),

    # path('addpage/', AddBook.as_view(), name='addbook'),
    path('uploadbook/', uploadbook, name='uploadbook'),
    path('deletebook/', deletebook, name='deletebook'),

    path('book/<slug:book_slug>', ShowBook.as_view(), name='book'),

    # path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),

    path('userBooksPage/<str:user>', UserBooksPage.as_view(), name='userBooksPage'),
    path('wishListPage/<str:user>', WishListPage.as_view(), name='wishListPage'),
    path('addToWishList', addToWishList, name='addToWishList'),

]
