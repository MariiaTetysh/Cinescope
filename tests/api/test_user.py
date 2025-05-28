import pytest

from models.model import User, UserCreation


class TestUser:

    @pytest.mark.smoke
    def test_create_user(self, super_admin, creation_user_data):
        """
        Тест на создание юзера c валидацей типов данных.
        """
        UserCreation(**creation_user_data)
        response = super_admin.api.user_api.create_user(
            creation_user_data
        ).json()
        user = User(**response)
        assert user.id and user.id != '', "ID должен быть не пустым"
        assert user.email == creation_user_data['email']
        assert user.fullName == creation_user_data['fullName']
        assert user.roles == creation_user_data['roles']
        assert user.verified is True

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        """
        Тест на получение информации о юзере по ID или Email.
        """
        created_user_response = super_admin.api.user_api.create_user(
            creation_user_data
        ).json()
        response_by_id = super_admin.api.user_api.get_user(
            created_user_response['id']
        ).json()
        response_by_email = super_admin.api.user_api.get_user(
            creation_user_data['email']
        ).json()

        assert response_by_id == response_by_email, (
            "Содержание ответов должно быть идентичным"
        )
        assert response_by_id.get('id') and response_by_id['id'] != '', (
            "ID должен быть не пустым"
        )
        assert response_by_id.get('email') == creation_user_data['email']
        assert response_by_id.get('fullName') == creation_user_data['fullName']
        assert response_by_id.get('roles', []) == creation_user_data['roles']
        assert response_by_id.get('verified') is True

    @pytest.mark.slow
    def test_get_user_by_id_common_user(self, common_user):
        """
        Тест на получение информации о юзере по Email c ролью "USER".
        """
        common_user.api.user_api.get_user(
            common_user.email, expected_status=403
        )

