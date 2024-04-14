from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

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
    try:
        post = Post.objects.get(slug=post_slug)
        post.views_count += 1
        post.save()

        comments = post.comments.all()
        comment_form = CommentForm()

    except Post.DoesNotExist:
        return render(request, 'app/404.html', status=404)
    except Exception:
        return render(request, 'app/500.html', status=500)

    return render(request, 'app/post_details.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

def comment(request):
    try:
        if request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                post_id = request.POST.get('post_id')
                post = Post.objects.get(id=post_id)
                comment.post = post
                comment.save()
                return HttpResponseRedirect(reverse('post_details', args=[post.slug]))

    except Post.DoesNotExist:
        return render(request, 'app/404.html', status=404)
    except Exception:
        return render(request, 'app/500.html', status=500)