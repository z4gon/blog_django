from django import forms
from app.models import Comment

class CommentForm(forms.ModelForm):
    """
    A form to represent a comment.
    """

    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']