from django.contrib import admin
from app.models import About, Author, ContactMessage, ContactInformation, Post, Subscription, Tag, Comment, User

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

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'bio')
    exclude = ('slug',)

class AboutAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'updated_at')

class ContactInformationAdmin(admin.ModelAdmin):
    list_display = ('email', 'address', 'phone', 'created_at', 'updated_at')

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'subject')

admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(About, AboutAdmin)
admin.site.register(ContactInformation, ContactInformationAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)