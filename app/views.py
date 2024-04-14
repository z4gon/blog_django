from django.shortcuts import render

from app.models import Post, Tag
from app.forms import CommentForm

# Create your views here.

def posts(request):
    if request.GET.get('tag'):
        tag_slug = request.GET.get('tag')
        try:
            tag = Tag.objects.get(slug=tag_slug)
        except Tag.DoesNotExist:
            return render(request, 'app/404.html', status=404)
        
        posts = tag.posts.all()[0:10]
        return render(request, 'app/tag_posts_list.html', {'tag': tag, 'posts': posts})
    else:
        posts = Post.objects.all()[0:10]
        return render(request, 'app/posts_list.html', {'posts': posts})

def post(request, post_slug):
    print('post request')

    if request.POST:
        print('request.POST')
        form = CommentForm(request.POST)
        if form.is_valid():
            print('CommentForm is valid')
            comment = form.save(commit=False)
            post_id = request.POST.get('post_id')
            post = Post.objects.get(id=post_id)
            comment.post = post
            comment.save()
        else:
            print('CommentForm is invalid ' + form.errors.as_json())
    else:
        print('No request.POST')
            
    try:
        post = Post.objects.get(slug=post_slug)
        post.views_count += 1
        post.save()
        comment_form = CommentForm()

    except Post.DoesNotExist:
        return render(request, 'app/404.html', status=404)

    return render(request, 'app/post_details.html', {'post': post, 'comment_form': comment_form})