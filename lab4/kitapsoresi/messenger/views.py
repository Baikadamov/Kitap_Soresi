from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

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


def show_book(request, book_id):
    return HttpResponse(f"id  = {book_id}")


def show_author(request, author_id):
    books = Books.objects.filter(author__id=author_id)
    genre = Genre.objects.all()
    author = Author.objects.all()
    context = {
        'books': books,
        'genre': genre,
        'author': author,
        'menu': menu,
        'author_selected': author_id,
    }
    return render(request, 'messenger/books.html', context=context)


def show_genre(request, genre_id):
    books = Books.objects.filter(genre__id=genre_id)
    genre = Genre.objects.all()
    author = Author.objects.all()
    context = {
        'books': books,
        'genre': genre,
        'author': author,
        'genre_selected': genre_id,
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
    genre = Genre.objects.all()
    author = Author.objects.all()
    context = {
        'books': books,
        'genre': genre,
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
