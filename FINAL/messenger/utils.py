from django.db.models import Count
from django.core.cache import cache
from .models import Genre, Books

menu = [
    {'title ': "Книги", 'url_name': 'books'},
    {'title': "О нас", 'url_name ': 'about'},
]


class DataMixin:
    paginate_by = 8

    def get_user_context(self, **kwargs):
        context = kwargs

        books_list = cache.get('books_list')

        genre = cache.get('genre')
        if not genre:
            genre = Genre.objects.annotate(Count('books'))
            cache.set('genre', genre, 60)

        if not books_list:
            books_list = Books.objects.annotate(Count('user'))
            cache.set('books_list', books_list, 60)

        context['menu'] = menu
        context['genre'] = genre
        context['books_list'] = books_list

        if 'genre_selected' not in context:
            context['genre_selected'] = 0
        return context


