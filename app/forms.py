from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from app.models import Comment, Subscription, ContactMessage

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

class ContactMessageForm(forms.ModelForm):
    """
    A form to represent a contact message.
    """

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

class SearchForm(forms.Form):
    """
    A form to represent a search query.
    """

    query = forms.CharField(max_length=200)

class RegisterForm(UserCreationForm):
    """
    A form to represent a user registration.
    """

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists.')
        return email