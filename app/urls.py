from app.views import PostsView, PostView, CommentView, SubscriptionView, SearchView, AboutView, ContactView, RegistrationView, BookmarkView, LikeView
from django.urls import path, include

urlpatterns = [
    path('', PostsView.as_view(), name='posts_list'),
    path('posts/', PostsView.as_view(), name='filtered_posts_list'),
    path('post/<slug:post_slug>', PostView.as_view(), name='post_details'),
    path('comment', CommentView.as_view(), name='comment'),
    path('subscribe', SubscriptionView.as_view(), name='subscribe'),
    path('search', SearchView.as_view(), name='search'),
    path('about', AboutView.as_view(), name='about'),
    path('contact', ContactView.as_view(), name='contact'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', RegistrationView.as_view(), name='register'),
    path('bookmark/<slug:post_slug>', BookmarkView.as_view(), name='bookmark'),
    path('like/<slug:post_slug>', LikeView.as_view(), name='like'),
]
