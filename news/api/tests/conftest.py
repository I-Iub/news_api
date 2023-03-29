import pytest
from rest_framework.test import APIClient

from ..models import Comment, News


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create(username='test_user',
                                            password='test_password')


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='test_author',
                                            password='test_password')


@pytest.fixture(scope='package')
def unauthorized_client():
    return APIClient()


@pytest.fixture
def authorized_client(django_user_model, user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def admin_client(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture
def author_client(author):
    client = APIClient()
    client.force_authenticate(user=author)
    return client


@pytest.fixture
def create_news(db, author):
    news = News.objects.create(title='test', text='test_text', author=author)
    yield news
    news.delete()


@pytest.fixture
def create_comment(db, create_news, author):
    comment = Comment.objects.create(
        text='test_comment', news=create_news, author=author
    )
    yield comment
    comment.delete()
