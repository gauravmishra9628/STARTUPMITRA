from django.contrib import admin
from .models import Post, PostLike, Comment, CommentLike


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'likes_count', 'comments_count', 'is_published', 'language', 'created_at']
    list_filter = ['category', 'is_published', 'language', 'created_at']
    search_fields = ['title', 'content', 'author__email']
    list_editable = ['is_published']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'content', 'likes_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'author__email']