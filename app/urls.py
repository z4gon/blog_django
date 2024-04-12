from app import views
from django.urls import path

urlpatterns = [
    path('', views.posts_list, name='posts_list'),
    path('post/<slug:post_slug>', views.post_details, name='post_details'),
    path('tag/<slug:tag_slug>', views.tag_posts_list, name='tag_posts_list'),
]
