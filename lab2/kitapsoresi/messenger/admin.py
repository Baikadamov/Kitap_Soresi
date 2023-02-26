from django.contrib import admin

# Register your models here.

from .models import *


# class BooksAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'photo', 'description', 'price', 'is_published')
#     list_display_links = ('id', 'name')
#     search_fields = ('name', 'description')
#     list_editable = ('is_published',)
#     list_filter = ('is_published',)
#
#
# class GenreAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')
#     list_display_links = ('id', 'name')
#     search_fields = ('name',)
#
#
# admin.site.register(Books, BooksAdmin)
# admin.site.register(Genre, GenreAdmin)
