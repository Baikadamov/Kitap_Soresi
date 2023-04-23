from django import forms
from django.forms import ModelForm

from social_book.models import Comment, ChatMessage


class ChatMessageForm(ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "rows": "3"}))

    class Meta:
        model = ChatMessage
        fields = ["body", ]
