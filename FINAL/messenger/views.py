# from msilib.schema import ListView
from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from form import form
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from messenger.forms import AddBookForm, RegisterUserForm, LoginUserForm
from messenger.models import Books, Author, WishList
from social_book.models import User, Post
from .permissons import IsAdminOrReadOnly
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
        if context['books']:
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


# class RegisterUser(DataMixin, CreateView):
#     form_class = RegisterUserForm
#     template_name = 'messenger/register.html'
#     success_url = reverse_lazy('profile')
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title="Регистрация")
#         return dict(list(context.items()) + list(c_def.items()))
#
#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('profile')


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


@login_required(login_url='signin')
def deletebook(request):
    if request.method == 'POST':
        pk = request.POST['pk']
        books = Books.objects.filter(id=pk)
        books.delete()
        return redirect('booksPage')
    return redirect('booksPage')


def uploadbook(request):
    author = Author.objects.all()
    genre = Genre.objects.all()
    context = {
        'menu': menu,
        'author': author,
        'genre': genre,
    }

    if request.method == 'POST':
        user = request.user
        photo = request.FILES.get('photo')
        name = request.POST['name']
        slug = request.POST['slug']
        author = request.POST['author']
        author = get_object_or_404(Author, pk=author)
        description = request.POST['description']
        genre_ids = request.POST.getlist('genre')
        price = request.POST['price']
        is_published = True
        try:
            books = Books.objects.create(name=name, slug=slug, author=author, description=description,
                                         price=price, is_published=is_published, photo=photo, user=user)
            books.genre.set(genre_ids)
            books.save()
        except IntegrityError:
            messages.error(request, 'An error occurred while saving your post. Please try again later.')
            return redirect(request.META['HTTP_REFERER'])

        return redirect('booksPage')
    else:
        return render(request, 'messenger/uploadbook.html', context=context)


# class AddBook(LoginRequiredMixin, DataMixin, CreateView):
#     form_class = AddBookForm
#     template_name = 'messenger/addbook.html'
#     success_url = reverse_lazy('booksPage')
#     login_url = reverse_lazy('home')
#     raise_exception = True
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title="add page")
#         return dict(list(context.items()) + list(c_def.items()))


class UserBooksPage(LoginRequiredMixin, DataMixin, ListView):
    model = Books
    template_name = 'messenger/user_books.html'
    # user = 'user'
    # slug_url_kwarg = 'user'
    context_object_name = 'books'

    def get_queryset(self):
        # print(self.kwargs['user'])
        us_id = User.objects.get(username=self.kwargs['user'])
        # return UserLib.objects.filter(user=self.request.user)
        return Books.objects.filter(user=us_id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Книги")
        context = dict(list(context.items()) + list(c_def.items()))
        return context


@login_required(login_url='signin')
def addToWishList(request):
    if request.method == 'POST':
        user = request.POST['user']
        user_id = User.objects.get(username=user)
        my_user_id = user_id.pk
        book_slug = request.POST['book_slug']
        print('my_data: ', user, user_id, book_slug)

        if WishList.objects.filter(user=user_id, book_slug=book_slug).first():
            delete_wish = WishList.objects.get(user=user_id, book_slug=book_slug)
            delete_wish.delete()
            return redirect('/main/wishListPage/' + user)
        else:
            new_wish = WishList.objects.create(user=user_id, book_slug=book_slug)
            new_wish.save()
            return redirect('/main/wishListPage/' + user)
    else:
        return render(request, 'messenger/user_wishList.html', )


class WishListPage(LoginRequiredMixin, DataMixin, ListView):
    model = WishList
    template_name = 'messenger/user_wishList.html'
    # user = 'user'
    # slug_url_kwarg = 'user'
    context_object_name = 'wish_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Желаемые Книги")
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        # print(self.kwargs['user'])
        us_id = User.objects.get(username=self.kwargs['user'])
        return WishList.objects.filter(user=us_id)


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


class BookAPIPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10000


class BooksViewSet(viewsets.ModelViewSet):
    # queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = BookAPIPagination

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        if not pk:
            return Books.objects.all()[:3]

        return Books.objects.filter(pk=pk)

    @action(methods=['get'], detail=True)
    def author(self, request, pk=None):
        author = Author.objects.get(pk=pk)
        return Response({'authors': author.name})


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        pk = self.kwargs.get("pk")

        if not pk:
            return Genre.objects.all()[:3]

        return Genre.objects.filter(pk=pk)


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        pk = self.kwargs.get("pk")

        if not pk:
            return Author.objects.all()[:3]

        return Author.objects.filter(pk=pk)


# class BooksAPIList(generics.ListCreateAPIView):
#     queryset = Books.objects.all()
#     serializer_class = BooksSerializer


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
        p = Author.objects.all()
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
