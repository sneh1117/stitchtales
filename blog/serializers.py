from rest_framework import serializers
from .models import Post, Category, Tag, Comment
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at', 'is_approved']
        read_only_fields = ['author', 'created_at', 'is_approved']


class PostListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'author', 'category', 'tags',
            'excerpt', 'cover_image', 'status', 'view_count',
            'reading_time', 'created_at', 'updated_at',
            'like_count', 'comment_count'
        ]
    
    def get_like_count(self, obj):
        return obj.likes.count()
    
    def get_comment_count(self, obj):
        return obj.comments.filter(is_approved=True).count()


class PostDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt', 'author',
            'category', 'tags', 'cover_image', 'status', 'view_count',
            'reading_time', 'created_at', 'updated_at', 'comments',
            'like_count', 'is_liked'
        ]
    
    def get_like_count(self, obj):
        return obj.likes.count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False