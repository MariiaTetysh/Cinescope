import pytest

from models.model import RegisterUserResponse, User, UserCreation


class TestUser:

    @pytest.mark.smoke
    def test_create_user(self, super_admin, creation_user_data_with_pydantic):
        """
        Тест на создание юзера c валидацей типов данных.
        """
        response = super_admin.api.user_api.create_user(
            creation_user_data_with_pydantic
        ).json()
        user = RegisterUserResponse(**response)
        assert user.id and user.id != '', "ID должен быть не пустым"
        assert user.email == creation_user_data_with_pydantic.email
        assert user.fullName == creation_user_data_with_pydantic.fullName
        assert user.roles == creation_user_data_with_pydantic.roles
        assert user.verified is True

    def test_get_user_by_locator(
        self, super_admin, creation_user_data_with_pydantic
    ):
        """
        Тест на получение информации о юзере по ID или Email.
        """
        created_user_response = super_admin.api.user_api.create_user(
            creation_user_data_with_pydantic
        ).json()
        response_by_id = super_admin.api.user_api.get_user(
            created_user_response['id']
        ).json()
        response_by_email = super_admin.api.user_api.get_user(
            creation_user_data_with_pydantic.email
        ).json()
        user_by_id = RegisterUserResponse(**response_by_id)
        user_by_email = RegisterUserResponse(**response_by_email)
        assert user_by_id == user_by_email, (
            "Содержание ответов должно быть идентичным"
        )
        assert user_by_id.id and user_by_id.id != '', (
            "ID должен быть не пустым"
        )
        assert user_by_id.email == creation_user_data_with_pydantic.email
        assert user_by_id.fullName == creation_user_data_with_pydantic.fullName
        assert user_by_id.roles == creation_user_data_with_pydantic.roles
        assert user_by_id.verified is True

    @pytest.mark.slow
    def test_get_user_by_id_common_user(self, common_user):
        """
        Тест на получение информации о юзере по Email c ролью "USER".
        """
        common_user.api.user_api.get_user(
            common_user.email, expected_status=403
        )
