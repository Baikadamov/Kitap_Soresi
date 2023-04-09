# from msilib.schema import ListView
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from messenger.forms import AddBookForm, RegisterUserForm, LoginUserForm
from messenger.models import Books, Genre, Author
from .utils import *

menu = [
    {'title ': "Книги", 'url_name': 'books'},
    {'title': "О нас", 'url_name ': 'about'},
]


# Create your views here.

def index(request):
    contact_list = Books.objects.all()

    books = Books.objects.all()

    context = {
        'title': 'General leaf',
        'menu': menu,
        'books': books,
    }
    return render(request, 'messenger/index.html', context=context)


class BookHome(DataMixin, ListView):
    model = Books
    template_name = 'messenger/books.html'
    context_object_name = 'books'

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Books page")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Books.objects.filter(is_published=True).prefetch_related('genre')


# def booksPage(requset):
#     books = Books.objects.all()
#     author = Author.objects.all()
#     context = {
#         'books': books,
#         'author': author,
#         'genre_selected': 0,
#         'author_selected': 0,
#         'menu': menu,
#     }
#     return render(requset, 'messenger/books.html', context=context)


class ShowBook(DataMixin, DetailView):
    model = Books
    template_name = 'messenger/book.html'
    slug_url_kwarg = 'book_slug'
    context_object_name = 'book'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['book'])
        return dict(list(context.items()) + list(c_def.items()))


# def show_book(request, book_slug):
#     book = get_object_or_404(Books, slug=book_slug)
#     context = {
#         'book': book,
#         'menu': menu,
#         # 'genre_selected': book.genre_id,
#     }
#
#     return render(request, 'messenger/book.html', context=context)


class BooksAuthor(ListView):
    model = Books
    template_name = 'messenger/books.html'
    context_object_name = 'books'
    allow_empty = True

    def get_queryset(self):
        return Books.objects.filter(author__slug=self.kwargs['author_slug'], is_published=True)

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genre_selected'] = 0
        context['author_selected'] = context['books'][0].author_id
        return context


# def show_author(request, author_slug):
#     books = Books.objects.filter(author__slug=author_slug)
#     # genre = Genre.objects.all()
#     # author = Author.objects.all()
#     context = {
#         'books': books,
#         # 'genre': genre,
#         # 'author': author,
#         'menu': menu,
#         'author_selected': author_slug,
#     }
#     return render(request, 'messenger/books.html', context=context)

class BooksGenre(DataMixin, ListView):
    model = Books
    template_name = 'messenger/books.html'
    context_object_name = 'books'
    allow_empty = True

    def get_queryset(self):
        return Books.objects.filter(genre__slug=self.kwargs['genre_slug'], is_published=True)

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genre_selected'] = 0
        context['author_selected'] = 0

        books = context.get('books', [])
        if books:
            genre = books[0].genre
            title = "Жанр - " + str(genre)
            c_def = self.get_user_context(title=title, genre_selected=genre)
            return dict(list(context.items()) + list(c_def.items()))

        return context


# def show_genre(request, genre_slug):
#     books = Books.objects.filter(genre__slug=genre_slug)
#     # author = Author.objects.all()
#     context = {
#         'books': books,
#         # 'author': author,
#         'genre_selected': genre_slug,
#         'menu': menu,
#     }
#     return render(request, 'messenger/books.html', context=context)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'messenger/register.html'
    success_url = reverse_lazy('profile')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('profile')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'messenger/login.html'
    success_url = reverse_lazy('profile')

    def get_success_url(self):
        return reverse_lazy('profile')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))


def logout_user(request):
    logout(request)
    return redirect('home')


class AddBook(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddBookForm
    template_name = 'messenger/addbook.html'
    success_url = reverse_lazy('booksPage')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="add page")
        return dict(list(context.items()) + list(c_def.items()))


# def addbook(request):
#     if request.method == 'POST':
#         form = AddBookForm(request.POST, request.FILES)
#         if form.is_valid():
#             print(form.cleaned_data)
#             form.save()
#             return redirect('booksPage')
#     else:
#         form = AddBookForm()
#
#     return render(request, 'messenger/addbook.html', {'form': form})

def profile(request):
    return render(request, 'messenger/profile.html')


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
