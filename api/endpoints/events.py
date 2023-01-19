from uuid import UUID
from fastapi import APIRouter, Form, Body
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.authentication import create_access_token, get_password_hash, verify_password, get_user_identity
from api.exceptions.common import ForbiddenException
from api.schemas.common import SuccessfullResponse, TokenOut, TokenIn
from migrations.database.connection.session import get_session
from api.schemas.events import EventOut, EventIn, UserEvent, EventNew
from api.schemas.users import UserOut
from api.services.users import get_user_by_email_or_phone
from api.services.events import get_user_event, get_event_users, get_user_events, create_new_event, delete_event, change_participation_status
from api.utils.formatter import serialize_models


event_router = APIRouter(tags=["Функции создателя"])


@event_router.get("/event/users", response_model=list[UserOut])
async def get_users_on_event(
    identity: str = Depends(get_user_identity),
    event: EventIn = Depends(),
    session: AsyncSession = Depends(get_session),
) -> list[UserOut]:
    user = await get_user_by_email_or_phone(identity,session)
    event = await get_user_event(user, event, session)
    users = await get_event_users(user, event, session)
    return serialize_models(users, UserOut)


@event_router.post("/event", response_model=SuccessfullResponse)
async def create_event(
    identity: str = Depends(get_user_identity),
    event_new: EventNew = Depends(),
    session: AsyncSession = Depends(get_session),
) -> SuccessfullResponse:
    user = await get_user_by_email_or_phone(identity, session)
    await create_new_event(user, event_new, session)
    return SuccessfullResponse()


@event_router.delete('/event', response_model=SuccessfullResponse)
async def delete_event_by_id(
    identity: str = Depends(get_user_identity),
    event_in: EventIn = Depends(),
    session: AsyncSession = Depends(get_session)
) -> SuccessfullResponse:
    user = await get_user_by_email_or_phone(identity, session)
    await delete_event(user, event_in, session)
    return SuccessfullResponse()


@event_router.put("/user/event/status", response_model=SuccessfullResponse)
async def change_payment_status(
    identity: str = Depends(get_user_identity),
    user_event: UserEvent = Depends(),
    session: AsyncSession = Depends(get_session)
) -> SuccessfullResponse:
    user = await get_user_by_email_or_phone(identity, session)
    await change_participation_status(user, user_event, session)
    return SuccessfullResponse()


@event_router.get('/user/events', response_model=list[EventOut])
async def get_created_events(
    identity: str = Depends(get_user_identity),
    session: AsyncSession = Depends(get_session)
) -> list[EventOut]:
    user = await get_user_by_email_or_phone(identity, session)
    events = await get_user_events(user, session)
    return serialize_models(events, EventOut)
