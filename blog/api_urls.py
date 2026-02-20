from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .api_views import PostViewSet, CategoryViewSet, TagViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', obtain_auth_token, name='api_token_auth'),
]