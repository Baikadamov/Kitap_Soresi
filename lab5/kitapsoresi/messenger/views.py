from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404

from messenger.models import Books, Genre, Author

menu = [
    {'title ': "Книги", 'url_name': 'books'},
    {'title': "О нас", 'url_name ': 'about'},
]


# Create your views here.

def index(request):
    context = {
        'title': 'General leaf',
        'menu': menu,
    }
    return render(request, 'messenger/index.html', context=context)


def show_book(request, book_slug):
    book = get_object_or_404(Books, slug=book_slug)
    context = {
        'book': book,
        'menu': menu,
        # 'genre_selected': book.genre_id,

    }

    return render(request, 'messenger/book.html', context=context)


def show_author(request, author_slug):
    books = Books.objects.filter(author__slug=author_slug)
    # genre = Genre.objects.all()
    # author = Author.objects.all()
    context = {
        'books': books,
        # 'genre': genre,
        # 'author': author,
        'menu': menu,
        'author_selected': author_slug,
    }
    return render(request, 'messenger/books.html', context=context)


def show_genre(request, genre_slug):
    books = Books.objects.filter(genre__slug=genre_slug)
    # author = Author.objects.all()
    context = {
        'books': books,
        # 'author': author,
        'genre_selected': genre_slug,
        'menu': menu,
    }
    return render(request, 'messenger/books.html', context=context)


def registrationPage(request):
    context = {
        'title': 'Registration Page',
        # 'menu':menu
    }
    return HttpResponseNotFound('<h1>Reg page</h1>')
    # return render(request, 'messenger/registrationPage.html', context=context)


def booksPage(requset):
    books = Books.objects.all()
    author = Author.objects.all()
    context = {
        'books': books,
        'author': author,
        'genre_selected': 0,
        'author_selected': 0,
        'menu': menu,
    }
    return render(requset, 'messenger/books.html', context=context)


def about(request):
    return HttpResponse('<h1>about</h1>')
    # return render(request, 'messenger/errors/500.html', status=500)


def categories(request, catid):
    return HttpResponse(f"<h1>Categories<br></h1>  <p>{catid}</p>")


def error400(request, exception):
    return HttpResponseNotFound('<h1>Page not found 400</h1>')
    # return render(request, 'messenger/errors/400.html', status=400)


def error403(request, exception):
    return HttpResponseNotFound('<h1>Page not found 403 </h1>')
    # return render(request, 'messenger/errors/403.html', status=403)


def error404(request, exception):
    return HttpResponseNotFound('<h1>Page not found 404</h1>')


def error500(request):
    return HttpResponseNotFound('<h1>Page not found 500</h1>')
    # return render(request, 'messenger/errors/500.html', status=500)
