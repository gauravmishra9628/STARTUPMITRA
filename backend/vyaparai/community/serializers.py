from rest_framework import serializers
from .models import Post, PostLike, Comment, CommentLike
from accounts.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment"""
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    author_avatar = serializers.ImageField(source='author.avatar', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_name', 'author_avatar', 'content', 'parent', 'likes_count', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post"""
    author_details = UserSerializer(source='author', read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'author_details', 'title', 'content', 'category',
            'likes_count', 'comments_count', 'views_count', 'language',
            'is_liked', 'created_at', 'updated_at'
        ]

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return PostLike.objects.filter(user=request.user, post=obj).exists()
        return False


class PostLikeSerializer(serializers.ModelSerializer):
    """Serializer for PostLike"""
    class Meta:
        model = PostLike
        fields = ['id', 'user', 'post', 'created_at']