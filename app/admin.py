from django.contrib import admin
from app.models import Post, Tag, Comment

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'content')
    exclude = ('slug', 'views_count')

admin.site.register(Post, PostAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    exclude = ('slug',)

admin.site.register(Tag, TagAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'created_at')

    # This will help you to disbale add functionality
    def has_add_permission(self, request):
        return False

    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Comment, CommentAdmin)