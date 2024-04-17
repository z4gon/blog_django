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
