import datetime

from rest_framework import status

url = '/api/v1/news/'
url_template = url + '%(news_id)s/comments/'


class TestGetNews:
    def test_unauthorized_client_get_news(
            self, unauthorized_client, create_news
    ):
        response = unauthorized_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = unauthorized_client.get(url + f'{create_news.id}/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_admin_client_get_news(
            self, admin_client, create_news
    ):
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        response = admin_client.get(url + f'{create_news.id}/')
        assert response.status_code == status.HTTP_200_OK

    def test_authorized_client_get_news(
            self, authorized_client, create_news
    ):
        response = authorized_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        response = authorized_client.get(url + f'{create_news.id}/')
        assert response.status_code == status.HTTP_200_OK

    def test_author_client_get_news(
            self, author_client, create_news
    ):
        response = author_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        response = author_client.get(url + f'{create_news.id}/')
        assert response.status_code == status.HTTP_200_OK

    def test_response_items_list(self, authorized_client, create_news):
        response = authorized_client.get(url)
        news_items = response.json().get('results')
        assert isinstance(news_items, list)
        assert len(news_items) == 1

    def test_news_list_fields(self, authorized_client, create_news):
        response = authorized_client.get(url)
        news_item = response.json().get('results')[0]
        assert 'pk' in news_item
        assert 'title' in news_item
        assert 'text' in news_item
        assert 'author' in news_item
        assert 'likes' in news_item
        assert 'published' in news_item
        assert 'num_comments' in news_item

    def test_news_detail_fields(self, authorized_client, create_news):
        response = authorized_client.get(url + f'{create_news.id}/')
        news_item = response.json()
        assert 'pk' in news_item
        assert 'title' in news_item
        assert 'text' in news_item
        assert 'author' in news_item
        assert 'likes' in news_item
        assert 'published' in news_item
        assert 'num_comments' in news_item

    def test_created_news_returns_in_response(
            self, authorized_client, create_news
    ):
        response = authorized_client.get(url)
        news_item = response.json().get('results')[0]
        assert news_item.get('title') == 'test'
        assert news_item.get('text') == 'test_text'
        assert news_item.get('author') == create_news.author.id
        assert news_item.get('likes') == 0
        assert news_item.get('num_comments') == 0


class TestPostNews:
    def test_unauthorized_client_post_news(self, unauthorized_client):
        data = dict(title='test_title', text='test_news')
        response = unauthorized_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_admin_client_post_news(self, create_news, admin_client):
        data = dict(title='test_title', text='test_news')
        response = admin_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_authorized_client_post_news(self, authorized_client):
        data = dict(title='test_title', text='test_news')
        response = authorized_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_authorized_client_post_news_duplicate(
            self, authorized_client
    ):
        data = dict(title='test_title', text='test_news')
        duplicate = dict(title='test_title', text='another_text')
        response = authorized_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        response = authorized_client.post(url, duplicate)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_response_item(self, authorized_client, user):
        data = dict(title='test_title', text='test_news')
        response = authorized_client.post(url, data)
        assert 'pk' in response.json()
        assert response.json().get('title') == 'test_title'
        assert response.json().get('text') == 'test_news'
        assert response.json().get('author') == user.id
        assert response.json().get('likes') == 0
        published = response.json().get('published')
        assert isinstance(
            datetime.datetime.strptime(published, '%Y-%m-%dT%H:%M:%S.%fZ'),
            datetime.datetime
        )


class TestPutNews:
    data = dict(title='test_put_title', text='test_put_news')

    def test_unauthorized_client_put_news(
            self, create_news, unauthorized_client
    ):
        detail_url = url + f'{create_news.id}/'
        response = unauthorized_client.put(detail_url, self.data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_admin_client_put_news(self, create_news, admin_client):
        detail_url = url + f'{create_news.id}/'
        response = admin_client.put(detail_url, self.data)
        assert response.status_code == status.HTTP_200_OK

    def test_not_author_client_put_news(self, create_news, authorized_client):
        detail_url = url + f'{create_news.id}/'
        response = authorized_client.put(detail_url, self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_author_client_put_news(self, create_news, author_client):
        detail_url = url + f'{create_news.id}/'
        response = author_client.put(detail_url, self.data)
        assert response.status_code == status.HTTP_200_OK

    def test_response_item(self, create_news, author_client, author):
        detail_url = url + f'{create_news.id}/'
        response = author_client.put(detail_url, self.data)
        assert 'pk' in response.json()
        assert response.json().get('title') == 'test_put_title'
        assert response.json().get('text') == 'test_put_news'
        assert response.json().get('author') == author.id
        assert response.json().get('likes') == 0
        published = response.json().get('published')
        assert isinstance(
            datetime.datetime.strptime(published, '%Y-%m-%dT%H:%M:%S.%fZ'),
            datetime.datetime
        )


class TestDeleteNews:
    def test_unauthorized_client_delete_news(
            self, create_news, unauthorized_client
    ):
        detail_url = url + f'{create_news.id}/'
        response = unauthorized_client.delete(detail_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_admin_client_delete_news(
            self, create_news, admin_client
    ):
        detail_url = url + f'{create_news.id}/'
        response = admin_client.delete(detail_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_author_client_delete_news(
            self, create_news, author_client
    ):
        detail_url = url + f'{create_news.id}/'
        response = author_client.delete(detail_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_not_author_client_delete_news(
            self, create_news, authorized_client
    ):
        detail_url = url + f'{create_news.id}/'
        response = authorized_client.delete(detail_url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestPostLike:
    def test_unauthorized_client_post_like(
            self, create_news, unauthorized_client
    ):
        like_url = url + f'{create_news.id}/like/'
        response = unauthorized_client.post(like_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_admin_client_post_like(
            self, create_news, admin_client
    ):
        like_url = url + f'{create_news.id}/like/'
        response = admin_client.post(like_url)
        assert response.status_code == status.HTTP_201_CREATED

    def test_authorized_client_post_like(
            self, create_news, authorized_client
    ):
        like_url = url + f'{create_news.id}/like/'
        response = authorized_client.post(like_url)
        assert response.status_code == status.HTTP_201_CREATED

    def test_author_client_post_like_own_news(
            self, create_news, author_client
    ):
        like_url = url + f'{create_news.id}/like/'
        response = author_client.post(like_url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data == {'error': 'Нельзя лайкать свою новость'}


class TestGetComments:
    def test_unauthorized_client_get_comments(
            self, unauthorized_client, create_news
    ):
        comments_url = url_template % {'news_id': create_news.id}
        response = unauthorized_client.get(comments_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_admin_client_get_comments(self, admin_client, create_news):
        comments_url = url_template % {'news_id': create_news.id}
        response = admin_client.get(comments_url)
        assert response.status_code == status.HTTP_200_OK

    def test_authorized_client_get_comments(
            self, authorized_client, create_comment, create_news
    ):
        comments_url = url_template % {'news_id': create_news.id}
        response = authorized_client.get(comments_url)
        assert response.status_code == status.HTTP_200_OK

    def test_author_client_get_comments(
            self, author_client, create_comment, create_news
    ):
        comments_url = url_template % {'news_id': create_news.id}
        response = author_client.get(comments_url)
        assert response.status_code == status.HTTP_200_OK

    def test_response_items(
            self, authorized_client, create_comment, create_news
    ):
        comments_url = url_template % {'news_id': create_news.id}
        response = authorized_client.get(comments_url)
        comment_items = response.json().get('results')
        assert isinstance(comment_items, list)
        assert len(comment_items) == 1

    def test_comments_list_fields(
            self, authorized_client, create_comment, create_news
    ):
        comments_url = url_template % {'news_id': create_news.id}
        response = authorized_client.get(comments_url)
        comment_item = response.json().get('results')[0]
        assert 'pk' in comment_item
        assert 'text' in comment_item
        assert 'author' in comment_item
        assert 'news' in comment_item
        assert 'published' in comment_item

    def test_created_comment_returns_in_response(
            self, authorized_client, create_comment, create_news
    ):
        comments_url = url_template % {'news_id': create_news.id}
        response = authorized_client.get(comments_url)
        comment_item = response.json().get('results')[0]
        assert comment_item.get('pk') == create_comment.id
        assert comment_item.get('text') == 'test_comment'
        assert comment_item.get('news') == create_news.id
