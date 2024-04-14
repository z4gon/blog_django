# Blog (Django 4.x)
A Blog built with Django 4

- [Blog (Django 4.x)](#blog-django-4x)
  - [Resources](#resources)
  - [Local Setup](#local-setup)
    - [Create Django Project](#create-django-project)
    - [Create Django App](#create-django-app)

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