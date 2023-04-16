from django import forms

from social_book.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('commenter_name', 'comment_body')
        widgets = {
            'commenter_name': forms.TextInput(attrs={'class': 'form-control'}),
            'comment_body': forms.Textarea(attrs={'class': 'form-control'}),
        }
