from app import views
from django.urls import path

urlpatterns = [
    path('', views.posts, name='posts_list'),
    path('posts/', views.posts, name='tag_posts_list'),
    path('post/<slug:post_slug>', views.post, name='post_details'),
]
