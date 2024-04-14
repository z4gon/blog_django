# Blog (Django 4.x)

A Blog built with Django 4

- [Blog (Django 4.x)](#blog-django-4x)
  - [Resources](#resources)
  - [Local Setup](#local-setup)
    - [Create Django Project](#create-django-project)
    - [Create Django App](#create-django-app)
  - [Custom Auth User](#custom-auth-user)

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

## Custom Auth User

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
