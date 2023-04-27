from django import template

from messenger.models import Books, Genre, Author

register = template.Library()


@register.simple_tag(name='get_genres')
def get_genre():
    return Genre.objects.all()


@register.inclusion_tag('messenger/tags/list_genres.html')
def show_genres(sort=None, genre_selected=0):
    if not sort:
        genres = Genre.objects.all()
    else:
        genres = Genre.objects.order_by(sort)

    return {"genres": genres, "genre_selected": genre_selected}


@register.inclusion_tag('messenger/tags/list_authors.html')
def show_authors(sort=None, author_selected=0):
    if not sort:
        author = Author.objects.all()
    else:
        author = Author.objects.order_by(sort)

    return {"author": author, "author_selected": author_selected}
