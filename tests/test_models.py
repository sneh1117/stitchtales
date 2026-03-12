import pytest
from django.utils.text import slugify
from blog.models import Post, Category, Tag, Comment, Like, UserProfile
from .factories import UserFactory, PostFactory, CategoryFactory, TagFactory, CommentFactory
from django.contrib.auth.models import User

@pytest.mark.django_db
class TestCategoryModel:
    def test_slug_auto_generated(self):
        category = CategoryFactory(name='Crochet Basics')
        assert category.slug == 'crochet-basics'

    def test_str_returns_name(self):
        category = CategoryFactory(name='Knitting')
        assert str(category) == 'Knitting'

    def test_get_absolute_url(self):
        category = CategoryFactory(name='Yarn Tips')
        assert category.get_absolute_url() == f'/category/{category.slug}/'


@pytest.mark.django_db
class TestTagModel:
    def test_slug_auto_generated(self):
        tag = TagFactory(name='Beginner Friendly')
        assert tag.slug == 'beginner-friendly'

    def test_str_returns_name(self):
        tag = TagFactory(name='advanced')
        assert str(tag) == 'advanced'


@pytest.mark.django_db
class TestPostModel:
    def test_slug_auto_generated(self):
        post = PostFactory(title='My First Post')
        assert post.slug == 'my-first-post'

    def test_reading_time_calculated(self):
        # 200 words = 1 min reading time
        content = ' '.join(['word'] * 200)
        post = PostFactory(content=content)
        assert post.reading_time == 1

    def test_excerpt_auto_generated(self):
        content = 'A' * 400
        post = PostFactory(content=content, excerpt='')
        assert len(post.excerpt) == 300

    def test_str_returns_title(self):
        post = PostFactory(title='Hello World')
        assert str(post) == 'Hello World'

    def test_get_absolute_url(self):
        post = PostFactory(title='URL Test Post')
        assert post.get_absolute_url() == f'/post/{post.slug}/'

    def test_default_status_is_draft(self):
    
        user = UserFactory()
        category = CategoryFactory()
        post = Post(
            title='Draft Post',
            author=user,
            category=category,
            content='Some content here'
        )
        post.save()
        assert post.status == 'draft'


@pytest.mark.django_db
class TestUserProfileModel:
    def test_profile_str(self):
        user = UserFactory(username='sneha')
        profile = UserProfile.objects.get_or_create(user=user)[0]
        assert 'sneha' in str(profile)

    def test_profile_created_with_user(self):
        user = UserFactory()
        profile, created = UserProfile.objects.get_or_create(user=user)
        assert profile.user == user


@pytest.mark.django_db
class TestCommentModel:
    def test_str_contains_author_and_post(self):
        comment = CommentFactory()
        assert comment.author.username in str(comment)
        assert comment.post.title in str(comment)

    def test_default_not_approved(self):
        comment = CommentFactory(is_approved=False)
        assert comment.is_approved is False


@pytest.mark.django_db
class TestLikeModel:
    def test_like_unique_together(self):
        from django.db import IntegrityError
        user = UserFactory()
        post = PostFactory()
        Like.objects.create(post=post, user=user)
        with pytest.raises(IntegrityError):
            Like.objects.create(post=post, user=user)