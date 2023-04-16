from django.db import models
from django.urls import reverse


# Create your models here.

class Genre(models.Model):
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('genre', kwargs={'genre_slug': self.slug})

    class Meta:
        verbose_name = 'Жанры книг'
        verbose_name_plural = 'Жанры книг'
        ordering = ['name']


class Author(models.Model):
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    name = models.CharField(max_length=200, help_text="Enter a book Author")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('author', kwargs={'author_slug': self.slug})

    class Meta:
        verbose_name = 'Авторы книг'
        verbose_name_plural = 'Автор книги'
        ordering = ['name']


class Books(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название книги")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    price = models.IntegerField(blank=False)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('book', kwargs={'book_slug': self.slug})

    class Meta:
        verbose_name = 'Список книг'
        verbose_name_plural = 'Список книг'
        ordering = ['name']
