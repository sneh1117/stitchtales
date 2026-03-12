import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .factories import UserFactory, PostFactory, CategoryFactory, TagFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client():
    user = UserFactory()
    token = Token.objects.create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return client, user


@pytest.mark.django_db
class TestPostAPI:
    def test_list_posts_public(self, api_client):
        PostFactory.create_batch(3, status='published')
        response = api_client.get('/api/posts/')
        assert response.status_code == 200
        assert response.data['count'] == 3

    def test_draft_posts_hidden_from_public(self, api_client):
        PostFactory(status='draft')
        PostFactory(status='published')
        response = api_client.get('/api/posts/')
        assert response.data['count'] == 1

    def test_get_single_post(self, api_client):
        post = PostFactory(status='published')
        response = api_client.get(f'/api/posts/{post.slug}/')
        assert response.status_code == 200
        assert response.data['title'] == post.title

    def test_write_operations_not_allowed(self, api_client):
        category = CategoryFactory()
        response = api_client.post('/api/posts/', {
            'title': 'Should Fail',
            'content': 'Content',
            'status': 'draft',
            'category': category.id,
        })
        assert response.status_code in [401, 405]

    def test_like_post_requires_auth(self, api_client):
        post = PostFactory(status='published')
        response = api_client.post(f'/api/posts/{post.slug}/like/')
        assert response.status_code == 401

    def test_like_post_authenticated(self, authenticated_client):
        client, user = authenticated_client
        post = PostFactory(status='published')
        response = client.post(f'/api/posts/{post.slug}/like/')
        assert response.status_code == 201
        assert response.data['status'] == 'liked'

    def test_unlike_post(self, authenticated_client):
        client, user = authenticated_client
        post = PostFactory(status='published')
        client.post(f'/api/posts/{post.slug}/like/')
        response = client.post(f'/api/posts/{post.slug}/like/')
        assert response.data['status'] == 'unliked'

    def test_comment_on_post_authenticated(self, authenticated_client):
        client, user = authenticated_client
        post = PostFactory(status='published')
        response = client.post(f'/api/posts/{post.slug}/comment/', {
            'content': 'Great post!'
        })
        assert response.status_code == 201

    def test_comment_requires_auth(self, api_client):
        post = PostFactory(status='published')
        response = api_client.post(f'/api/posts/{post.slug}/comment/', {
            'content': 'Should fail'
        })
        assert response.status_code == 401

@pytest.mark.django_db
class TestCategoryAPI:
    def test_list_categories(self, api_client):
        CategoryFactory.create_batch(3)
        response = api_client.get('/api/categories/')
        assert response.status_code == 200
        assert response.data['count'] == 3

    def test_get_single_category(self, api_client):
        category = CategoryFactory(name='Knitting')
        response = api_client.get(f'/api/categories/{category.slug}/')
        assert response.status_code == 200
        assert response.data['name'] == 'Knitting'


@pytest.mark.django_db
class TestTagAPI:
    def test_list_tags(self, api_client):
        TagFactory.create_batch(4)
        response = api_client.get('/api/tags/')
        assert response.status_code == 200
        assert response.data['count'] == 4


@pytest.mark.django_db
class TestTokenAuth:
    def test_obtain_token_valid_credentials(self, api_client):
        user = UserFactory()
        response = api_client.post('/api/auth/token/', {
            'username': user.username,
            'password': 'testpass123',
        })
        assert response.status_code == 200
        assert 'token' in response.data

    def test_obtain_token_invalid_credentials(self, api_client):
        response = api_client.post('/api/auth/token/', {
            'username': 'nobody',
            'password': 'wrongpass',
        })
        assert response.status_code == 400