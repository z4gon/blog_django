from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.

# https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#substituting-a-custom-user-model
# class User(AbstractUser):
#     slug = models.SlugField(max_length=200, unique=True)

#     def __str__(self):
#         return self.username
    
#     def save(self, *args, **kwargs):
#         if not self.id: # only on creation
#             self.slug = slugify(self.username)

#         return super().save(*args, **kwargs)
    
class Tag(models.Model):
    """
    A model to represent a tag.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.id: # only on creation
            self.slug = slugify(self.name)

        return super().save(*args, **kwargs)
    
class Post(models.Model):
    """
    A model to represent a blog post.
    """
    
    # auto_now_add=True
    #     means that the field will be automatically set to now when the object is first created.
    #     https://docs.djangoproject.com/en/4.2/ref/models/fields/#django.db.models.DateField.auto_now_add

    # auto_now=True
    #     means that the field will be automatically set to now every time the object is saved.
    #     https://docs.djangoproject.com/en/4.2/ref/models/fields/#django.db.models.DateField.auto_now

    # blank=True
    #     means that the field is allowed to be blank, like an empty string.
    #     https://docs.djangoproject.com/en/4.2/ref/models/fields/#django.db.models.Field.blank

    # null=True
    #     means that the field is allowed to be null.
    #     https://docs.djangoproject.com/en/4.2/ref/models/fields/#django.db.models.Field.null

    title = models.CharField(max_length=200)
    body = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    views_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    # relationships
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    # author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title
    
    # https://docs.djangoproject.com/en/4.2/topics/db/models/#overriding-model-methods
    def save(self, *args, **kwargs):
        if not self.id: # only on creation
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)
    
class Comment(models.Model):
    """
    A model to represent a comment.
    """

    # on_delete=models.CASCADE
    #     means that the comment will be deleted if the post is deleted.
    #     https://docs.djangoproject.com/en/4.2/ref/models/fields/#django.db.models.ForeignKey.on_delete

    name = models.CharField(max_length=200)
    email = models.EmailField()
    body = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # relationships
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, blank=True, null=True, related_name='replies')
    # author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name + ' - ' + self.post.title
    
class Subscription(models.Model):
    """
    A model to represent a subscription
    """

    email = models.EmailField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email