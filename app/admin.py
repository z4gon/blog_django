from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app.models import Post, Subscription, Tag, Comment, User

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'content')
    exclude = ('slug', 'views_count')

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    exclude = ('slug',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'parent', 'created_at')

    def has_add_permission(self, request):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False
    
    def has_change_permission(self, request, obj=None):
        return False

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email',)

admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Subscription, SubscriptionAdmin)

# https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#substituting-a-custom-user-model
# admin.site.register(User, UserAdmin)