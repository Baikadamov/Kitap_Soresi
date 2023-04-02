from django.contrib import admin

# Register your models here.

from .models import *


class BooksAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'photo', 'description', 'price', 'is_published', 'get_genre',  )
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')
    list_editable = ('is_published',)
    list_filter = ('is_published',)
    prepopulated_fields = {"slug": ("name",)}

    def get_genre(self, obj):
        return [genre.name for genre in obj.genre.all()]



class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Books, BooksAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Author, AuthorAdmin)
