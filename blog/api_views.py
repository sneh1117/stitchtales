from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Post, Category, Tag, Comment, Like
from .serializers import (
    PostListSerializer, PostDetailSerializer,
    CategorySerializer, TagSerializer, CommentSerializer
)


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for posts.
    List: GET /api/posts/
    Detail: GET /api/posts/{slug}/
    """
    queryset = Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'excerpt']
    ordering_fields = ['created_at', 'view_count', 'title']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostListSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, slug=None):
        """
        Like/unlike a post
        POST /api/posts/{slug}/like/
        """
        post = self.get_object()
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        
        if not created:
            like.delete()
            return Response({
                'status': 'unliked',
                'like_count': post.likes.count()
            })
        
        return Response({
            'status': 'liked',
            'like_count': post.likes.count()
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def comment(self, request, slug=None):
        """
        Add a comment to a post
        POST /api/posts/{slug}/comment/
        Body: {"content": "Your comment here"}
        """
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for categories.
    List: GET /api/categories/
    Detail: GET /api/categories/{slug}/
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    
    @action(detail=True, methods=['get'])
    def posts(self, request, slug=None):
        """
        Get all posts in a category
        GET /api/categories/{slug}/posts/
        """
        category = self.get_object()
        posts = Post.objects.filter(category=category, status='published')
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for tags.
    List: GET /api/tags/
    Detail: GET /api/tags/{slug}/
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'
    
    @action(detail=True, methods=['get'])
    def posts(self, request, slug=None):
        """
        Get all posts with a tag
        GET /api/tags/{slug}/posts/
        """
        tag = self.get_object()
        posts = Post.objects.filter(tags=tag, status='published')
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)