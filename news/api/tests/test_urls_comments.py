import datetime

from rest_framework import status

from ..models import Comment

url = '/api/v1/comments/'


class TestGetComments:
    def test_unauthorized_client_get_comments(self, unauthorized_client):
        response = unauthorized_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_admin_client_get_comments(self, admin_client):
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_authorized_client_get_comments(
            self, authorized_client, create_comment
    ):
        response = authorized_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_author_client_get_comments(
            self, author_client, create_comment
    ):
        response = author_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_response_items(self, authorized_client, create_comment):
        response = authorized_client.get(url)
        comment_items = response.json().get('results')
        assert isinstance(comment_items, list)
        assert len(comment_items) == 1

    def test_comments_list_fields(
            self, authorized_client, create_comment
    ):
        response = authorized_client.get(url)
        comment_item = response.json().get('results')[0]
        assert 'pk' in comment_item
        assert 'text' in comment_item
        assert 'author' in comment_item
        assert 'news' in comment_item
        assert 'published' in comment_item

    def test_created_comment_returns_in_response(
            self, authorized_client, create_comment, create_news
    ):
        response = authorized_client.get(url)
        comment_item = response.json().get('results')[0]
        assert comment_item.get('pk') == create_comment.id
        assert comment_item.get('text') == 'test_comment'
        assert comment_item.get('news') == create_news.id


class TestPostComment:
    def test_unauthorized_client_post_comment(
            self, create_news, unauthorized_client
    ):
        data = dict(text='test_comment', news=create_news.id)
        response = unauthorized_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_admin_client_post_comment(self, create_news, admin_client):
        data = dict(text='test_comment', news=create_news.id)
        response = admin_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_authorized_client_post_comment(
            self, create_news, authorized_client
    ):
        data = dict(text='test_comment', news=create_news.id)
        response = authorized_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_response_item(self, create_news, authorized_client, user):
        data = dict(text='test_comment', news=create_news.id)
        response = authorized_client.post(url, data)
        assert 'pk' in response.json()
        assert response.json().get('text') == 'test_comment'
        assert response.json().get('author') == user.id
        assert response.json().get('news') == create_news.id
        published = response.json().get('published')
        assert isinstance(
            datetime.datetime.strptime(published, '%Y-%m-%dT%H:%M:%S.%fZ'),
            datetime.datetime
        )


class TestDeleteComment:
    def test_unauthorized_client_delete_comment(
            self, create_comment, unauthorized_client
    ):
        response = unauthorized_client.delete(url + f'{create_comment.id}/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_admin_client_delete_comment(
            self, create_comment, admin_client
    ):
        response = admin_client.delete(url + f'{create_comment.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Comment.objects.filter(id=create_comment.id).exists()

    def test_author_delete_comment(
            self, create_comment, author_client
    ):
        response = author_client.delete(url + f'{create_comment.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Comment.objects.filter(id=create_comment.id).exists()

    def test_not_author_delete_comment(
            self, create_comment, authorized_client
    ):
        response = authorized_client.delete(url + f'{create_comment.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Comment.objects.filter(id=create_comment.id).exists()
