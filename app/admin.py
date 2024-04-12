from django.contrib import admin
from app.models import Post

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'content')
    exclude = ('slug',)

admin.site.register(Post, PostAdmin)