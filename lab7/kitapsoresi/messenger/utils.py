from django.db.models import Count

from .models import Genre

menu = [
    {'title ': "Книги", 'url_name': 'books'},
    {'title': "О нас", 'url_name ': 'about'},
]


class DataMixin:
    paginate_by = 3
    def get_user_context(self, **kwargs):
        context = kwargs
        genre = Genre.objects.annotate(Count('books'))
        context['menu'] = menu
        context['genre'] = genre
        if 'genre_selected' not in context:
            context['genre_selected'] = 0
        return context
