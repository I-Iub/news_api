import datetime

from rest_framework import status

from ..models import Comment

url = '/api/v1/comments/'


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
