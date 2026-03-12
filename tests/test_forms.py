import pytest
from django.contrib.auth.models import User
from blog.forms import RegisterForm, UserUpdateForm, PostForm, CommentForm
from .factories import UserFactory, CategoryFactory


@pytest.mark.django_db
class TestRegisterForm:
    def get_valid_data(self):
        return {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }

    def test_valid_form(self):
        form = RegisterForm(data=self.get_valid_data())
        assert form.is_valid(), form.errors

    def test_missing_email(self):
        data = self.get_valid_data()
        data.pop('email')
        form = RegisterForm(data=data)
        assert not form.is_valid()
        assert 'email' in form.errors

    def test_password_mismatch(self):
        data = self.get_valid_data()
        data['password2'] = 'WrongPassword!'
        form = RegisterForm(data=data)
        assert not form.is_valid()

    def test_duplicate_username(self):
        UserFactory(username='taken')
        data = self.get_valid_data()
        data['username'] = 'taken'
        form = RegisterForm(data=data)
        assert not form.is_valid()
        assert 'username' in form.errors


@pytest.mark.django_db
class TestUserUpdateForm:
    def test_valid_form(self):
        user = UserFactory()
        form = UserUpdateForm(data={
            'username': user.username,
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'Name',
        }, instance=user)
        assert form.is_valid(), form.errors

    def test_invalid_email(self):
        user = UserFactory()
        form = UserUpdateForm(data={
            'username': user.username,
            'email': 'not-an-email',
            'first_name': 'Test',
            'last_name': 'User',
        }, instance=user)
        assert not form.is_valid()
        assert 'email' in form.errors


@pytest.mark.django_db
class TestPostForm:
    def test_valid_form(self):
        category = CategoryFactory()
        form = PostForm(data={
            'title': 'Test Post Title',
            'category': category.id,
            'content': 'This is the post content with enough words.',
            'excerpt': 'Short excerpt.',
            'status': 'draft',
            'tags': [],
        })
        assert form.is_valid(), form.errors

    def test_missing_title(self):
        category = CategoryFactory()
        form = PostForm(data={
            'category': category.id,
            'content': 'Some content',
            'status': 'draft',
        })
        assert not form.is_valid()
        assert 'title' in form.errors

    def test_missing_content(self):
        category = CategoryFactory()
        form = PostForm(data={
            'title': 'A Title',
            'category': category.id,
            'status': 'draft',
        })
        assert not form.is_valid()
        assert 'content' in form.errors


@pytest.mark.django_db
class TestCommentForm:
    def test_valid_form(self):
        form = CommentForm(data={'content': 'Great post!'})
        assert form.is_valid()

    def test_empty_content(self):
        form = CommentForm(data={'content': ''})
        assert not form.is_valid()
        assert 'content' in form.errors