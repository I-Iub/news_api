import pytest
from rest_framework import status

url = '/api/v1/users/'


class TestPostUser:
    @pytest.mark.django_db
    def test_create_user(self, unauthorized_client):
        data = {'username': 'new_test_user', 'password': 'test_user_password'}
        response = unauthorized_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_user_with_existing_username(
            self, unauthorized_client, user
    ):
        data = {'username': user.username, 'password': 'test_user_password'}
        response = unauthorized_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestDeleteUser:
    delete_url = url + 'delete/'

    def test_unauthorized_client_delete(self, unauthorized_client):
        response = unauthorized_client.delete(self.delete_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authorized_client_delete(self, authorized_client):
        response = authorized_client.delete(self.delete_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
