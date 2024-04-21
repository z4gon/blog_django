# Blog (Django 4.x)

A Blog built with Django 4

- [Blog (Django 4.x)](#blog-django-4x)
  - [Resources](#resources)
  - [Local Setup](#local-setup)
    - [Create Django Project](#create-django-project)
    - [Create Django App](#create-django-app)
  - [Auth Users](#auth-users)
    - [Extending existing User Model](#extending-existing-user-model)
    - [Custom Auth User](#custom-auth-user)
  - [ORM](#orm)
    - [Complex Queries](#complex-queries)
  - [Sessions](#sessions)
    - [Store Session Data](#store-session-data)
  - [Auth](#auth)
    - [URLs](#urls)
    - [Login](#login)
    - [Log Out](#log-out)
    - [Register](#register)
      - [Custom Errors](#custom-errors)
      - [Upload Profile Image](#upload-profile-image)

## Resources

[Python Django 4 Masterclass | Build a Real World Project](https://www.udemy.com/course/python-django-masterclass)
[ZenBlog - Bootstrap Blog Template](https://bootstrapmade.com/zenblog-bootstrap-blog-template/)

## Local Setup

- [pyenv](https://github.com/pyenv/pyenv)
- [pipenv](https://pipenv.pypa.io/en/latest/)

### Create Django Project

```sh
pipenv install django==4.2.11 pillow==10.3.0
pipenv shell
django-admin startproject blog_project .
python ./manage.py runserver
```

### Create Django App

```sh
python ./manage.py startapp app
```

## Views

```py
# views.py

from django.views import View

class ContactView(View):
    def get(self, request):
        ...
        
    def post(self, request):
        ...
```

```py
# urls.py

from app.views import ContactView

urlpatterns = [
    path('contact/', ContactView.as_view(), name='contact'),
]
```

## Auth Users

### Extending existing User Model

```py
# models.py
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
```

### Custom Auth User

See the [doc](https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#substituting-a-custom-user-model)

```py
# settings.py
AUTH_USER_MODEL = "myapp.MyUser"
```

```py
# models.py

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
```

```py
# admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)
```

## ORM

### Complex Queries

Read the [doc](https://docs.djangoproject.com/en/4.2/topics/db/queries/#complex-lookups-with-q-objects)

```py
from django.db.models import Q

# OR
posts = Post.objects.filter(
    Q(title__icontains=q_text) | Q(body__icontains=q_text)
)[0:MAX_POSTS]
```

## Sessions

### Store Session Data

```html
<!-- subscription_form.html -->
{% if subscription_form and not request.session.subscribed %} ... {% endif %}
```

```py
# views.py

def subscribe(request):
    if request.method == "POST":
        ...
        if form.is_valid():
            ...
            request.session["subscribed"] = True
```

## Auth

### URLs

```py
# urls.py

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
]
```

It will add all the necessary urls:

```
accounts/ login/ [name='login']
accounts/ logout/ [name='logout']
accounts/ password_change/ [name='password_change']
accounts/ password_change/done/ [name='password_change_done']
accounts/ password_reset/ [name='password_reset']
accounts/ password_reset/done/ [name='password_reset_done']
accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/ reset/done/ [name='password_reset_complete']
```

But the templates need to be provided:

```
TemplateDoesNotExist at /accounts/login/
registration/login.html
```

### Login

```py
# settings.py

LOGIN_REDIRECT_URL = '/'
```

```html
<!-- app/templates/registration/login.html -->

<form action="{% url 'login' %}" method="post" role="form">
	{% csrf_token %}
	<input
		name="{{ form.username.html_name }}"
		id="{{ form.username.auto_id }}"
	/>
	<input
		name="{{ form.password.html_name }}"
		id="{{ form.password.auto_id }}"
	/>
	{% if form.non_field_errors %} {% for error in form.non_field_errors %}
	<div class="alert alert-danger" role="alert">{{ error }}</div>
	{% endfor %} {% endif %}
	<button type="submit" class="rounded">Login</button>
</form>
```

### Log Out

Move all the admin apps below the auth app,
so that the logout url from the app takes precedence

```py
# settings.py

INSTALLED_APPS = [
    'django.contrib.auth',
    ...
    'jazzmin',
    'django.contrib.admin',
]
```

```html
<!-- app/templates/base.html -->

<div class="position-relative d-flex align-items-center">
	{% if request.user.is_authenticated %}
	<p class="logged-in-user">
		Welcome, <strong>{{ request.user.username }}</strong>!
	</p>
	<a href="{% url 'logout' %}" class="logo d-flex align-items-center">
		<button class="btn btn-primary">Log Out</button>
	</a>
	{% else %}
	<a href="{% url 'login' %}" class="logo d-flex align-items-center">
		<button class="btn btn-primary">Login</button>
	</a>
	{% endif %}
</div>
```

Override the `logged_out.html` template

### Register

```py
# urls.py

path('accounts/register', views.register, name='register'),
```

```py
# forms.py
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    """
    A form to represent a user registration.
    """

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
```

```py
# views.py

from django.contrib.auth import authenticate, login
from app.forms import RegisterForm

def register(request):
    try:
        if request.POST:
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                user = authenticate(username=register_form.cleaned_data.get('username'), password=register_form.cleaned_data.get('password1'))
                author = Author(
                    user=user,
                    image=''
                )
                author.save()
                if user:
                    login(request, user)
                    return HttpResponseRedirect(reverse('posts_list'))
            else:
                return render(request, 'registration/registration.html', {'register_form': register_form})

        register_form = RegisterForm()
        return render(request, 'registration/registration.html', {'register_form': register_form})

    except Exception as e:
        print(e)
        return render(request, 'app/500.html', status=500)
```

#### Custom Errors

```py
# forms.py

class RegisterForm(UserCreationForm):
    ...

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
```

#### Upload Profile Image

```py
# validators.py

import os
from django.core.exceptions import ValidationError

def validate_image_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Supported extensions are .jpg and .png.')
```

```py
# forms.py

from app.validators import validate_image_file_extension

class RegisterForm(UserCreationForm):
    ...

    image = forms.ImageField(required=True, validators=[validate_image_file_extension])
```

```py
# views.py

from blog_django import settings

def register(request):
    try:
        if request.POST:
            register_form = RegisterForm(request.POST, request.FILES)
            if register_form.is_valid():
                ...

                image_file = register_form.cleaned_data.get('image')
                handle_uploaded_image(image_file)
                author = Author(
                    user=user,
                    image=f"images/{image_file.name}"
                )
                author.save()

                ...

def handle_uploaded_image(file):
    # save file in storage using the MEDIA_ROOT
    with open(f"{settings.MEDIA_ROOT}/images/{file.name}", 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
```