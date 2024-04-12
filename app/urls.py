from app import views
from django.urls import path

urlpatterns = [
    path('', views.posts, name='posts'),
    path('post/<slug:post_slug>', views.post, name='post'),
]
