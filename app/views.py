from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login

from app.models import About, Author, Comment, ContactInformation, Post, Tag
from app.forms import CommentForm, ContactMessageForm, SubscriptionForm, SearchForm, RegisterForm

# Create your views here.

MAX_POSTS = 50
MAX_FOOTER_TAGS = 5

common_props = {
    'subscription_form': SubscriptionForm(),
    'search_form': SearchForm(),
    'footer_tags': Tag.objects.all()[0:MAX_FOOTER_TAGS]
}

def posts(request):
    try:
        if request.GET.get('tag'):
            tag_slug = request.GET.get('tag')
            tag = Tag.objects.get(slug=tag_slug)
            posts = tag.posts.all()[0:MAX_POSTS]
            return render(request, 'app/tag_posts_list.html', {'tag': tag, 'posts': posts, **common_props})
        elif request.GET.get('author'):
            author_slug = request.GET.get('author')
            author = Author.objects.get(slug=author_slug)
            posts = author.posts.all()[0:MAX_POSTS]
            return render(request, 'app/author_posts_list.html', {'author': author, 'posts': posts, **common_props})
        elif request.GET.get('q'):
            q_text = request.GET.get('q')
            posts = Post.objects.filter(
                Q(title__icontains=q_text) | Q(body__icontains=q_text)
            )[0:MAX_POSTS]
            return render(request, 'app/search_results_posts_list.html', {'q_text': q_text, 'posts': posts, **common_props})
        else:
            popular_posts = Post.objects.all().order_by('-views_count')[0:MAX_POSTS]
            latest_posts = Post.objects.all()[0:MAX_POSTS]
            return render(request, 'app/posts_list.html', {'popular_posts': popular_posts, 'latest_posts': latest_posts, **common_props})

    except (Tag.DoesNotExist, Author.DoesNotExist):
        return render(request, 'app/404.html', status=404)
    except Exception as e:
        print(e)
        return render(request, 'app/500.html', status=500)
    
def post(request, post_slug):
    try:
        post = Post.objects.get(slug=post_slug)
        post.views_count += 1
        post.save()

        comments = post.comments.filter(parent=None)
        comment_form = CommentForm()

    except Post.DoesNotExist:
        return render(request, 'app/404.html', status=404)
    except Exception:
        return render(request, 'app/500.html', status=500)

    return render(request, 'app/post_details.html', {'post': post, 'root_comments': comments, 'comment_form': comment_form, **common_props})

def comment(request):
    try:
        if request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)

                post_id = request.POST.get('post_id')
                post = Post.objects.get(id=post_id)
                comment.post = post

                if request.POST.get('parent_id'):
                    parent_id = request.POST.get('parent_id')
                    parent = Comment.objects.get(id=parent_id)
                    comment.parent = parent

                comment.save()

                return HttpResponseRedirect(reverse('post_details', args=[post.slug]))

    except (Post.DoesNotExist, Comment.DoesNotExist):
        return render(request, 'app/404.html', status=404)
    except Exception:
        return render(request, 'app/500.html', status=500)
    
def subscribe(request):
    try:
        if request.POST:
            form = SubscriptionForm(request.POST)
            if form.is_valid():
                form.save()
                request.session['subscribed'] = True
                return render(request, 'app/subscription_successful.html')

    except Exception:
        return render(request, 'app/500.html', status=500)
    

def search(request):
    try:
        if request.POST:
            form = SearchForm(request.POST)
            if form.is_valid():
                return HttpResponseRedirect(reverse('filtered_posts_list') + '?q=' + form.cleaned_data.get('query'))

    except Exception:
        return render(request, 'app/500.html', status=500) 
    

def about(request):
    try:
        about = About.objects.all()[0:1][0]
        return render(request, 'app/about.html', {'about': about, **common_props})

    except Exception:
        return render(request, 'app/500.html', status=500) 
    

def contact(request):
    try:
        if request.POST:
            contact_message_form = ContactMessageForm(request.POST)
            if contact_message_form.is_valid():
                contact_message_form.save()
                return render(request, 'app/contact_message_successful.html')
            
        contact_info = ContactInformation.objects.all()[0:1][0]
        contact_message_form = ContactMessageForm()
        return render(request, 'app/contact.html', {'contact_info': contact_info, 'contact_message_form': contact_message_form,  **common_props})

    except Exception:
        return render(request, 'app/500.html', status=500) 
    

def register(request):
    try:
        if request.POST:
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                user = authenticate(username=register_form.cleaned_data.get('username'), password=register_form.cleaned_data.get('password1'))
                author = Author(
                    user=user,
                    image=''
                )
                author.save()
                if user:
                    login(request, user)
                    return HttpResponseRedirect(reverse('posts_list'))
            else:
                return render(request, 'registration/registration.html', {'register_form': register_form})
            
        register_form = RegisterForm()
        return render(request, 'registration/registration.html', {'register_form': register_form})

    except Exception as e:
        print(e)
        return render(request, 'app/500.html', status=500) 
        