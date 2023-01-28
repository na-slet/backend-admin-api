from migrations.database.models import Users, Events, Participations
from migrations.database.models.credentials import CredentialTypes

from api.exceptions.common import BadRequest, NotFoundException, InternalServerError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, and_, or_,delete, update
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from api.schemas.events import EventIn, EventNew, UserEvent, EventOut


async def get_user_event(user: Users, event: EventIn, session: AsyncSession) -> Events:
    try:
        query = select(Events).where(
            and_(
                Events.id == str(event.id),
                Events.creator_id == str(user.id)
            )
        )
        result = (await session.execute(query)).scalars().first()
        if not result:
            raise NotFoundException("Event not found")
        return result
    except IntegrityError as e:
        raise InternalServerError(e) from e


async def get_user_events(user: Users, session: AsyncSession) -> list[Events]:
    try:
        query = select(Events).where(
            Events.creator_id == str(user.id)
        )
        result = (await session.execute(query)).scalars().all()
        return result
    except IntegrityError as e:
        raise InternalServerError(e) from e


async def get_event_users(user: Users, event: EventIn, session: AsyncSession) -> list[(Users,Participations)]:
    query = select(Users, Participations).join(
        Participations, Users.id == Participations.user_id
    ).join(
        Events, Events.id == Participations.event_id
    ).where(
        and_(
            Participations.event_id == str(event.id),
            Events.creator_id == str(user.id)
        )
    )
    return (await session.execute(query)).all()


async def create_new_event(user: Users, event: EventNew, session: AsyncSession) -> None:
    try:
        query = insert(Events).values(
            name=event.name,
            description=event.description,
            short_description=event.short_description,
            **({'visibility': event.visibility} if event.visibility else {}),
            price=event.price,
            logo_variant=event.logo_variant,
            city=event.city,
            reg_end_date=event.reg_end_date,
            start_date=event.start_date,
            end_date=event.end_date,
            total_places=event.total_places,
            url_link=event.url_link,
            category_type=event.category_type,
            event_type=event.event_type,
            **({'union_id': str(event.union_id)} if event.union_id else {}),
            min_age=event.min_age,
            max_age=event.max_age,
            address=event.address,
            latitude=event.latitude,
            longitude=event.longitude,
            creator_id=str(user.id)
        )
        await session.execute(query)
        await session.commit()
    except IntegrityError as e:
        raise InternalServerError(e) from e


async def delete_event(user: Users, user_event: EventIn, session: AsyncSession) -> None:
    try:
        query = delete(Events).where(and_(
            Events.id == str(user_event.id),
            Events.creator_id == str(user.id)
        ))
        await session.execute(query)
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise InternalServerError(e) from e


async def change_participation_status(user: Users, user_event: UserEvent, session: AsyncSession) -> None:
    try:
        query = update(Participations).values(
            participation_stage=user_event.stage
        ).where(and_(
            Participations.user_id == str(user.id),
            Participations.event_id == str(user_event.id),
        ))
        await session.execute(query)
        await session.commit()
    except IntegrityError as e:
        raise InternalServerError(e) from e


async def update_event(user: Users, user_event: EventOut, session: AsyncSession) -> None:
    try:
        query = update(Events).values(
            name=func.coalesce(user_event.name, Events.name),
            description=func.coalesce(user_event.description, Events.description),
            short_description=func.coalesce(user_event.short_description, Events.short_description),
            visibility=func.coalesce(user_event.visibility, Events.visibility),
            price=func.coalesce(user_event.price, Events.price),
            logo_variant=func.coalesce(user_event.logo_variant, Events.logo_variant),
            city=func.coalesce(user_event.city, Events.city),
            reg_end_date=func.coalesce(user_event.reg_end_date, Events.reg_end_date),
            start_date=func.coalesce(user_event.start_date, Events.start_date),
            end_date=func.coalesce(user_event.end_date, Events.end_date),
            total_places=func.coalesce(user_event.total_places, Events.total_places),
            url_link=func.coalesce(user_event.url_link, Events.url_link),
            category_type=func.coalesce(user_event.category_type, Events.category_type),
            event_type=func.coalesce(user_event.event_type, Events.event_type),
            union_id=func.coalesce(user_event.union_id, Events.union_id),
            min_age=func.coalesce(user_event.min_age, Events.min_age),
            max_age=func.coalesce(user_event.max_age, Events.max_age),
            address=func.coalesce(user_event.address, Events.address),
            latitude=func.coalesce(user_event.latitude, Events.latitude),
            longitude=func.coalesce(user_event.longitude, Events.longitude),
        ).where(and_(
            Events.creator_id == str(user.id),
            Events.id == str(user_event.id)
        ))
        await session.execute(query)
        await session.commit()
    except IntegrityError as e:
        raise InternalServerError(e) from e