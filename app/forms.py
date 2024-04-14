from django import forms
from app.models import Comment, Subscription

class CommentForm(forms.ModelForm):
    """
    A form to represent a comment.
    """

    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

class SubscriptionForm(forms.ModelForm):
    """
    A form to represent a subscription.
    """

    class Meta:
        model = Subscription
        fields = ['email']