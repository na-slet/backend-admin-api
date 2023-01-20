
from uuid import UUID
from enum import Enum
from datetime import date
from pydantic import BaseModel, Field
from migrations.database.models.users import Genders
from migrations.database.models.events import EventType


class UserProfile(BaseModel):
    first_name: str = Field(None, description='Имя пользователя')
    last_name: str = Field(None, description='Фамилия пользователя')
    gender: str = Field(None, description='Пол пользователя')
    phone: str = Field(None, description='Телефон пользователя')
    email: str = Field(None, description='Почта пользователя')
    city: str = Field(None, description='Город пользователя')
    tg_link: str = Field(None, description='Ссылка на Telegram пользователя')
    birth_date: str = Field(None, description='Дата рождения пользователя')

    class Config:
        orm_mode = True


class UserOut(UserProfile):
    status: EventType = Field(None, description='Статус на слёте')
    payment_id: str = Field(None, description='Ссылка на оплату')

    class Config:
        orm_mode = True