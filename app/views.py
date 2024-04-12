from django.shortcuts import render

from app.models import Post, Tag

# Create your views here.

def posts_list(request):
    posts = Post.objects.all()[0:10]
    return render(request, 'app/posts_list.html', {'posts': posts})

def post_details(request, post_slug):
    try:
        post = Post.objects.get(slug=post_slug)
        post.views_count += 1
        post.save()
    except Post.DoesNotExist:
        return render(request, 'app/404.html', status=404)

    return render(request, 'app/post_details.html', {'post': post})

def tag_posts_list(request, tag_slug):
    try:
        tag = Tag.objects.get(slug=tag_slug)
    except Tag.DoesNotExist:
        return render(request, 'app/404.html', status=404)
    
    posts = tag.posts.all()[0:10]
    return render(request, 'app/tag_posts_list.html', {'tag': tag, 'posts': posts})