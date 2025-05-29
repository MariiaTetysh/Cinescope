from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Roles(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    USER = "USER"


class MovieLocation(str, Enum):
    MSK = "MSK"
    SPB = "SPB"


class UserRegistration(BaseModel):
    email: str
    fullName: str
    password: str = Field(min_length=8)
    passwordRepeat: str = Field(min_length=8)
    roles: list[str]


class UserCreation(BaseModel):
    fullName: str
    email: str
    password: str = Field(min_length=8)
    banned: Optional[bool] = Field(default=False)
    verified: Optional[bool] = Field(default=True)

    @field_validator("email")
    def check_email(cls, value: str) -> str:
        """
        Проверяем, есть ли знак "@" в email.
        """
        if '@' not in value:
            raise ValueError('Email должен содержать в себе знак "@"')
        return value

class User(BaseModel):
    id: str = Field(..., description='Идентификатор пользователя')
    email: str
    fullName: str
    roles: list[Roles]
    verified: bool = Field(default=True)
    createdAt: str = Field(default='2024-03-02T05:37:47.298Z')
    banned: bool = Field(default=False)


class TestUser(BaseModel):
    email: str
    fullName: str
    password: str
    passwordRepeat: str = Field(
        ..., min_length=1, max_length=20,
        description="passwordRepeat должен совпадать с полем password"
    )
    roles: list[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value
    
    # Добавляем кастомный JSON-сериализатор для Enum
    class Config:
        json_encoders = {
            Roles: lambda v: v.value  # Преобразуем Enum в строку
        }
    
class RegisterUserResponse(BaseModel):
    id: str
    email: str = Field(
        pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        description="Email пользователя"
    )
    fullName: str = Field(
        min_length=1, max_length=100, description="Полное имя пользователя"
    )
    verified: bool
    banned: bool
    roles: list[Roles]
    createdAt: str = Field(
        description="Дата и время создания пользователя в формате ISO 8601"
    )

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        # Валидатор для проверки формата даты и времени (ISO 8601).
        try:
            datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени")
        return value



class MovieCreation(BaseModel):
    name: str = Field(default='Название фильма')
    imageUrl: Optional[str] = Field(default='https://image.url')
    price: int = Field(default=100)
    description: str = Field(default='Описание фильма')
    location: MovieLocation
    published: bool = Field(default=True)
    genreId: int = Field(default=1)


class Movie(BaseModel):
    id: int
    name: str
    price: int = Field(..., gt=0, description="Цена должна быть положительной")
    description: str
    imageUrl: str = Field(..., pattern=r'^https?://')
    location: MovieLocation
    published: bool
    genreId: int
    genre: dict
    createdAt: str = Field(default='2024-03-02T05:37:47.298Z')
    rating: float = Field(
        ..., ge=0, le=5, description="Рейтинг должен быть от 0 до 5"
    )
