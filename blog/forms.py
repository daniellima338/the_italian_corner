from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """ Form for the comments"""
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
