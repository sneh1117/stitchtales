import pytest
from django.urls import reverse
from django.test import Client
from .factories import UserFactory, PostFactory, CategoryFactory, TagFactory, CommentFactory


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def logged_in_client():
    user = UserFactory()
    client = Client()
    client.force_login(user)
    return client, user


@pytest.mark.django_db
class TestHomeView:
    def test_home_returns_200(self, client):
        response = client.get(reverse('home'))
        assert response.status_code == 200

    def test_home_shows_published_posts(self, client):
        post = PostFactory(status='published')
        response = client.get(reverse('home'))
        assert post.title in str(response.content)

    def test_home_hides_draft_posts(self, client):
        post = PostFactory(status='draft')
        response = client.get(reverse('home'))
        assert post.title not in str(response.content)


@pytest.mark.django_db
class TestPostDetailView:
    def test_published_post_returns_200(self, client):
        post = PostFactory(status='published')
        response = client.get(reverse('post_detail', kwargs={'slug': post.slug}))
        assert response.status_code == 200

    def test_draft_post_returns_404(self, client):
        post = PostFactory(status='draft')
        response = client.get(reverse('post_detail', kwargs={'slug': post.slug}))
        assert response.status_code == 404

    def test_view_count_increments(self, client):
        post = PostFactory(status='published', view_count=0)
        client.get(reverse('post_detail', kwargs={'slug': post.slug}))
        post.refresh_from_db()
        assert post.view_count == 1


@pytest.mark.django_db
class TestAuthViews:
    def test_login_page_returns_200(self, client):
        response = client.get(reverse('login'))
        assert response.status_code == 200

    def test_register_page_returns_200(self, client):
        response = client.get(reverse('register'))
        assert response.status_code == 200

    def test_valid_login_redirects(self, client):
        user = UserFactory()
        response = client.post(reverse('login'), {
            'username': user.username,
            'password': 'testpass123',
        })
        assert response.status_code == 302

    def test_invalid_login_stays_on_page(self, client):
        response = client.post(reverse('login'), {
            'username': 'nobody',
            'password': 'wrongpassword',
        })
        assert response.status_code == 200

    def test_register_creates_user(self, client):
        from django.contrib.auth.models import User
        response = client.post(reverse('register'), {
            'username': 'brandnewuser',
            'email': 'new@example.com',
            'first_name': 'Brand',
            'last_name': 'New',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        assert User.objects.filter(username='brandnewuser').exists()


@pytest.mark.django_db
class TestDashboardView:
    def test_dashboard_requires_login(self, client):
        response = client.get(reverse('dashboard'))
        assert response.status_code == 302

    def test_dashboard_accessible_when_logged_in(self, logged_in_client):
        client, user = logged_in_client
        response = client.get(reverse('dashboard'))
        assert response.status_code == 200

    def test_dashboard_shows_only_own_posts(self, logged_in_client):
        client, user = logged_in_client
        own_post = PostFactory(author=user, status='published')
        other_post = PostFactory(status='published')
        response = client.get(reverse('dashboard'))
        assert own_post.title in str(response.content)
        assert other_post.title not in str(response.content)


@pytest.mark.django_db
class TestPostCreateView:
    def test_create_requires_login(self, client):
        response = client.get(reverse('post_create'))
        assert response.status_code == 302

    def test_create_post(self, logged_in_client):
        client, user = logged_in_client
        category = CategoryFactory()
        response = client.post(reverse('post_create'), {
            'title': 'Brand New Post',
            'category': category.id,
            'content': 'This is some content for the post.',
            'status': 'draft',
            'tags': [],
        })
        from blog.models import Post
        assert Post.objects.filter(title='Brand New Post').exists()


@pytest.mark.django_db
class TestPostDeleteView:
    def test_author_can_delete(self, logged_in_client):
        client, user = logged_in_client
        post = PostFactory(author=user)
        response = client.post(reverse('post_delete', kwargs={'slug': post.slug}))
        from blog.models import Post
        assert not Post.objects.filter(slug=post.slug).exists()

    def test_non_author_cannot_delete(self, logged_in_client):
        client, user = logged_in_client
        other_post = PostFactory()
        response = client.post(reverse('post_delete', kwargs={'slug': other_post.slug}))
        from blog.models import Post
        assert Post.objects.filter(slug=other_post.slug).exists()


@pytest.mark.django_db
class TestSearchView:
    def test_search_returns_200(self, client):
        response = client.get(reverse('search') + '?q=test')
        assert response.status_code == 200

    def test_search_finds_post_by_title(self, client):
        post = PostFactory(title='Unique Crochet Tutorial', status='published')
        response = client.get(reverse('search') + '?q=Unique+Crochet')
        assert post.title in str(response.content)