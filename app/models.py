from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    # auto_now_add=True means that the field will be automatically set to now when the object is first created.
    # https://docs.djangoproject.com/en/4.2/ref/models/fields/#django.db.models.DateField.auto_now_add
    created_at = models.DateTimeField(auto_now_add=True) 
    # auto_now=True means that the field will be automatically set to now every time the object is saved.
    # https://docs.djangoproject.com/en/4.2/ref/models/fields/#django.db.models.DateField.auto_now
    updated_at = models.DateTimeField(auto_now=True) 
    slug = models.SlugField(max_length=200, unique=True)
    # blank=True means that the field is allowed to be blank, like an empty string.
    # https://docs.djangoproject.com/en/4.2/ref/models/fields/#django.db.models.Field.blank
    # null=True means that the field is allowed to be null.
    # https://docs.djangoproject.com/en/4.2/ref/models/fields/#django.db.models.Field.null
    image = models.ImageField(upload_to='images/', blank=True, null=True)