import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from blog.models import Category, Tag, Post, UserProfile, Comment


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')


class UserProfileFactory(DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = factory.SubFactory(UserFactory)
    bio = factory.Faker('text', max_nb_chars=200)


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f'Category {n}')
    description = factory.Faker('sentence')


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Sequence(lambda n: f'tag{n}')


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Sequence(lambda n: f'Test Post {n}')
    author = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    content = factory.Faker('text', max_nb_chars=500)
    status = 'published'


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    post = factory.SubFactory(PostFactory)
    author = factory.SubFactory(UserFactory)
    content = factory.Faker('text', max_nb_chars=200)
    is_approved = True