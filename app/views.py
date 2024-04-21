from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.views import View

from app.models import About, Author, Comment, ContactInformation, Post, Tag
from app.forms import CommentForm, ContactMessageForm, SubscriptionForm, SearchForm, RegisterForm
from blog_django import settings

# Create your views here.

MAX_POSTS = 50
MAX_FOOTER_TAGS = 5

common_props = {
    'subscription_form': SubscriptionForm(),
    'search_form': SearchForm(),
    'footer_tags': Tag.objects.all()[0:MAX_FOOTER_TAGS]
}

class PostsView(View):
    def get(self, request):
        try:
            if request.GET.get('tag'):
                tag_slug = request.GET.get('tag')
                tag = Tag.objects.get(slug=tag_slug)
                posts = tag.posts.all()[0:MAX_POSTS]

                context = {
                    'tag': tag,
                    'posts': posts,
                    **common_props
                }

                return render(request, 'app/tag_posts_list.html', context)
            elif request.GET.get('author'):
                author_slug = request.GET.get('author')
                author = Author.objects.get(slug=author_slug)
                posts = author.posts.all()[0:MAX_POSTS]

                context = {
                    'author': author,
                    'posts': posts,
                    **common_props
                }

                return render(request, 'app/author_posts_list.html', context)
            elif request.GET.get('q'):
                q_text = request.GET.get('q')
                posts = Post.objects.filter(
                    Q(title__icontains=q_text) | Q(body__icontains=q_text)
                )[0:MAX_POSTS]

                context = {
                    'q_text': q_text,
                    'posts': posts,
                    **common_props
                }

                return render(request, 'app/search_results_posts_list.html', context)
            else:
                popular_posts = Post.objects.all().order_by('-views_count')[0:MAX_POSTS]
                latest_posts = Post.objects.all()[0:MAX_POSTS]

                context = {
                    'popular_posts': popular_posts,
                    'latest_posts': latest_posts,
                    **common_props
                }

                return render(request, 'app/posts_list.html', context)

        except (Tag.DoesNotExist, Author.DoesNotExist):
            return render(request, 'app/404.html', status=404)
        except Exception as e:
            print(e)
            return render(request, 'app/500.html', status=500)

class PostView(View):
    def get(self, request, post_slug):
        try:
            post = Post.objects.get(slug=post_slug)
            post.views_count += 1
            post.save()

            is_bookmarked = False
            is_liked_by_user = False

            if request.user.is_authenticated:
                is_bookmarked = post.bookmarkers.filter(id=request.user.id).exists()
                is_liked_by_user = post.likers.filter(id=request.user.id).exists()

            comments = post.comments.filter(parent=None)
            comment_form = CommentForm()

        except Post.DoesNotExist:
            return render(request, 'app/404.html', status=404)
        except Exception:
            return render(request, 'app/500.html', status=500)
        
        context = {
            'post': post,
            'is_bookmarked': is_bookmarked,
            'is_liked_by_user': is_liked_by_user,
            'root_comments': comments,
            'comment_form': comment_form,
            **common_props
        }

        return render(request, 'app/post_details.html', context)

class CommentView(View):
    def post(self, request):
        try:
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

class SubscriptionView(View):
    def post(self, request):
        try:
            form = SubscriptionForm(request.POST)
            if form.is_valid():
                form.save()
                request.session['subscribed'] = True
                return render(request, 'app/subscription_successful.html')

        except Exception:
            return render(request, 'app/500.html', status=500)

class SearchView(View):
    def post(self, request):
        try:
            form = SearchForm(request.POST)
            if form.is_valid():
                return HttpResponseRedirect(reverse('filtered_posts_list') + '?q=' + form.cleaned_data.get('query'))

        except Exception:
            return render(request, 'app/500.html', status=500) 

class AboutView(View):
    def get(self, request):
        try:
            about = About.objects.all()[0:1][0]

            context = {
                'about': about,
                **common_props
            }

            return render(request, 'app/about.html', context)

        except Exception:
            return render(request, 'app/500.html', status=500) 

class ContactView(View):
    def get(self, request):
        try:
            contact_info = ContactInformation.objects.all()[0:1][0]
            contact_message_form = ContactMessageForm()

            context = {
                'contact_info': contact_info,
                'contact_message_form': contact_message_form,
                **common_props
            }

            return render(request, 'app/contact.html', context)

        except Exception:
            return render(request, 'app/500.html', status=500)
        
    def post(self, request):
        try:
            contact_message_form = ContactMessageForm(request.POST)
            if contact_message_form.is_valid():
                contact_message_form.save()
                return render(request, 'app/contact_message_successful.html')

        except Exception:
            return render(request, 'app/500.html', status=500)

class RegistrationView(View):
    def get(self, request):
        try:
            register_form = RegisterForm()

            context = {
                'register_form': register_form,
                **common_props
            }

            return render(request, 'registration/registration.html', context)

        except Exception:
            return render(request, 'app/500.html', status=500) 

    def post(self, request):
        try:
            register_form = RegisterForm(request.POST, request.FILES)
            if register_form.is_valid():
                # create user
                register_form.save()
                
                # authenticate
                user = authenticate(username=register_form.cleaned_data.get('username'), password=register_form.cleaned_data.get('password1'))

                # create author
                image_file = register_form.cleaned_data.get('image')
                self._handle_uploaded_image(image_file)
                author = Author(
                    user=user,
                    image=f"images/{image_file.name}"
                )
                author.save()

                if user:
                    login(request, user)
                    return HttpResponseRedirect(reverse('posts_list'))
            else:
                context = {
                    'register_form': register_form
                }

                return render(request, 'registration/registration.html', context)

        except Exception:
            return render(request, 'app/500.html', status=500)
        
    def _handle_uploaded_image(self, file):
        # save file in storage using the MEDIA_ROOT
        with open(f"{settings.MEDIA_ROOT}/images/{file.name}", 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

class BookmarkView(View):
    def get(self, request, post_slug):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login') + f"?next={reverse('post_details', args=[post_slug])}")

        try:
            post = Post.objects.get(slug=post_slug)

            if not post.bookmarkers.filter(id=request.user.id).exists():
                post.bookmarkers.add(request.user)
            else:
                post.bookmarkers.remove(request.user)

            return HttpResponseRedirect(reverse('post_details', args=[post_slug]))
        
        except Post.DoesNotExist:
            return render(request, 'app/404.html', status=404)
        
        except Exception:
            return render(request, 'app/500.html', status=500)

class BookmarksView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        try:
            posts = request.user.bookmarks.all()[0:MAX_POSTS]

            context = {
                'posts': posts,
                **common_props
            }

            return render(request, 'app/bookmarked_posts_list.html', context)

        except Exception:
            return render(request, 'app/500.html', status=500) 

class LikeView(View):
    def get(self, request, post_slug):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login') + f"?next={reverse('post_details', args=[post_slug])}")
        
        try:
            post = Post.objects.get(slug=post_slug)

            if not post.likers.filter(id=request.user.id).exists():
                post.likers.add(request.user)
                post.likes_count += 1
            else:
                post.likers.remove(request.user)
                post.likes_count -= 1
            
            post.save()

            return HttpResponseRedirect(reverse('post_details', args=[post_slug]))
        
        except Post.DoesNotExist:
            return render(request, 'app/404.html', status=404)
        
        except Exception:
            return render(request, 'app/500.html', status=500)
        

class LikesView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        try:
            posts = request.user.likes.all()[0:MAX_POSTS]

            context = {
                'posts': posts,
                **common_props
            }

            return render(request, 'app/liked_posts_list.html', context)

        except Exception:
            return render(request, 'app/500.html', status=500) 