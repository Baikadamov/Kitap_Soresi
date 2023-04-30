from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.

from .models import *


class BooksAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'photo', 'description', 'price', 'is_published', 'get_genre', 'get_html_photo',)
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')
    list_editable = ('is_published',)
    list_filter = ('is_published',) 
    prepopulated_fields = {"slug": ("name",)}

    def get_genre(self, obj):
        return [genre.name for genre in obj.genre.all()]

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src = '{object.photo.url}' width=50 >")

    get_html_photo.short_description = "МИНИАТЮРА"

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
admin.site.register(WishList)
