from django import forms
from django.core.exceptions import ValidationError

from .models import *


class AddBookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].empty_label = "Автор не выбран"

    class Meta:
        model = Books
        fields = ['name', 'slug', 'description', 'photo', 'author', 'genre', 'price', 'is_published', ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'genre': forms.CheckboxSelectMultiple(attrs={'class': ''}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 100:
            raise ValidationError('Длина превышает 100 символов')
        return name


    # name = forms.CharField(max_length=255, label='Название', widget=forms.TextInput(attrs={'class': 'form-control'}))
    # slug = forms.SlugField(max_length=255, label='Слаг', widget=forms.TextInput(attrs={'class': 'form-control'}))
    # author = forms.ModelChoiceField(queryset=Author.objects.all(),
    #                                 label='Автор', empty_label="Выберите автора",
    #                                 widget=forms.Select(attrs={'class': 'form-select'}))
    # description = forms.CharField(label='Описание', widget=forms.TextInput(attrs={'class': 'form-control'}))
    # genre = forms.ModelMultipleChoiceField(queryset=Genre.objects.all(),
    #                                        widget=forms.CheckboxSelectMultiple(attrs={'class': ''}),
    #                                        label='Жанр')
    # price = forms.IntegerField(label='Цена', widget=forms.TextInput(attrs={'class': 'form-control'}))
    # is_published = forms.BooleanField(initial=True)
