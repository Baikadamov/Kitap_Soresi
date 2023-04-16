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
from rest_framework.response import Response
from rest_framework.views import APIView

from messenger.forms import AddBookForm, RegisterUserForm, LoginUserForm
from messenger.models import Books, Genre, Author
from .serializers import BooksSerializer, GenreSerializer, AuthorSerializer
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


class ShowBook(DataMixin, DetailView):
    model = Books
    template_name = 'messenger/book.html'
    slug_url_kwarg = 'book_slug'
    context_object_name = 'book'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['book'])
        return dict(list(context.items()) + list(c_def.items()))


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


class BooksAPIView(APIView):
    def get(self, request):
        p = Books.objects.all()
        return Response({'books': BooksSerializer(p, many=True).data})

    def post(self, request):
        serializer = BooksSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'books': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method put not allowed"})

        try:
            instance = Books.objects.get(pk=pk)
        except:
            return Response({"error": "oBject doesnt not exists"})

        serializer = BooksSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"books": serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method DELETE not allowed"})

        try:
            record = Books.objects.get(pk=pk)
            record.delete()
        except:
            return Response({"error": "Object does not exists"})

        return Response({"books": "delete post " + str(pk)})


class GenreAPIView(APIView):
    def get(self, request):
        p = Genre.objects.all()
        return Response({'genre': GenreSerializer(p, many=True).data})

    def post(self, request):
        serializer = GenreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'genre': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method put not allowed"})

        try:
            instance = Genre.objects.get(pk=pk)
        except:
            return Response({"error": "oBject doesnt not exists"})

        serializer = GenreSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"genre": serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method DELETE not allowed"})

        try:
            record = Genre.objects.get(pk=pk)
            record.delete()
        except:
            return Response({"error": "Object does not exists"})

        return Response({"genre": "delete post " + str(pk)})


class AuthorAPIView(APIView):
    def get(self, request):
        p =  Author.objects.all()
        return Response({'author': AuthorSerializer(p, many=True).data})

    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'author': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method put not allowed"})

        try:
            instance = Author.objects.get(pk=pk)
        except:
            return Response({"error": "oBject doesnt not exists"})

        serializer = AuthorSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"author": serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method DELETE not allowed"})

        try:
            record = Author.objects.get(pk=pk)
            record.delete()
        except:
            return Response({"error": "Object does not exists"})

        return Response({"author": "delete post " + str(pk)})