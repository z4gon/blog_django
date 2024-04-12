from django.shortcuts import render

from app.models import Post

# Create your views here.

def posts(request):
    posts = Post.objects.all()[0:10]
    return render(request, 'app/posts.html', {'posts': posts})

def post(request, post_slug):
    try:
        post = Post.objects.get(slug=post_slug)
    except Post.DoesNotExist:
        return render(request, 'app/404.html', status=404)

    return render(request, 'app/post.html', {'post': post})