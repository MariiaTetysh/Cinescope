from pydantic import BaseModel, Field, field_validator
from enum import Enum
from typing import Optional


class UserRoles(str, Enum):
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
    password: str = Field(min_length=8)
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
    roles: list[UserRoles]
    verified: bool = Field(default=True)
    createdAt: str = Field(default='2024-03-02T05:37:47.298Z')
    banned: bool = Field(default=False)


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
