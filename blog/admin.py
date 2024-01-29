from django.contrib import admin
from .models import Post, Comment
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_filter = []
    list_display = ['author', 'timestamp']
    search_fields = ['author', 'timestamp', 'title', 'intro']
    readonly_fields = ['timestamp']

    ordering = ['-timestamp']

    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_filter = []
    list_display = ['author', 'post']
    search_fields = ['author', 'post']
    readonly_fields = ['timestamp']

    class Meta:
        model = Comment

admin.site.register(Comment, CommentAdmin)