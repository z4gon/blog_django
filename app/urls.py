from app import views
from django.urls import path, include

urlpatterns = [
    path('', views.posts, name='posts_list'),
    path('posts/', views.posts, name='filtered_posts_list'),
    path('post/<slug:post_slug>', views.post, name='post_details'),
    path('comment', views.comment, name='comment'),
    path('subscribe', views.subscribe, name='subscribe'),
    path('search', views.search, name='search'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('accounts/', include('django.contrib.auth.urls')),
]
