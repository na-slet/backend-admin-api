
from uuid import UUID
from enum import Enum
from datetime import date
from pydantic import BaseModel, Field
from migrations.database.models.users import Genders
from migrations.database.models.events import EventType
from api.schemas.events import Participation


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


class UserOut(BaseModel):
    id: UUID = Field(None, description='UUID пользователя')
    first_name: str = Field(None, description='Имя пользователя')
    last_name: str = Field(None, description='Фамилия пользователя')
    gender: Genders = Field(None, description='Пол пользователя')
    phone: str = Field(None, description='Телефон пользователя')
    parent_phone: str = Field(None, description='Телефон родителя')
    parent_fio: str = Field(None, description='ФИО родителя')
    parent_email: str = Field(None, description='Email родителя')
    email: str = Field(None, description='Почта пользователя')
    avatar_id: str = Field(None, description='Аватарка пользователя')
    city: str = Field(None, description='Город пользователя')
    tg_link: str = Field(None, description='Ссылка на Telegram пользователя')
    birth_date: date = Field(None, description='Дата рождения пользователя')
    union_id: UUID = Field(None, description='UUID объединения')

    class Config:
        orm_mode = True


class UserParticipation(BaseModel):
    participation: Participation
    user: UserOut
