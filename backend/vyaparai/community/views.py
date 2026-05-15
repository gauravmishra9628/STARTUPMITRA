from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Post, PostLike, Comment, CommentLike
from .serializers import PostSerializer, PostLikeSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for Community Posts"""
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Post.objects.filter(is_published=True).select_related('author')

        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        language = self.request.query_params.get('language')

        if category:
            queryset = queryset.filter(category=category)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )
        if language:
            queryset = queryset.filter(language=language)

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Like a post"""
        post = self.get_object()
        like, created = PostLike.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.delete()
            post.likes_count = max(0, post.likes_count - 1)
            post.save()
            return Response({'liked': False, 'likes_count': post.likes_count})

        post.likes_count += 1
        post.save()
        return Response({'liked': True, 'likes_count': post.likes_count})


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for Comments"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.request.query_params.get('post')
        if post_id:
            return Comment.objects.filter(post_id=post_id).select_related('author', 'parent')
        return Comment.objects.none()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Like a comment"""
        comment = self.get_object()
        like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)

        if not created:
            like.delete()
            comment.likes_count = max(0, comment.likes_count - 1)
            comment.save()
            return Response({'liked': False, 'likes_count': comment.likes_count})

        comment.likes_count += 1
        comment.save()
        return Response({'liked': True, 'likes_count': comment.likes_count})