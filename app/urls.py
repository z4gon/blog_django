from app import views
from django.urls import path

urlpatterns = [
    path('', views.posts_list, name='posts_list'),
    path('post/<slug:post_slug>', views.post_details, name='post_details'),
]
