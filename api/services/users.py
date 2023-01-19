from migrations.database.models import Users, Credentials
from migrations.database.models.credentials import CredentialTypes

from api.exceptions.common import BadRequest, NotFoundException, InternalServerError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, and_, or_
from sqlalchemy.exc import IntegrityError


async def get_user_by_email_or_phone(identity: str, session: AsyncSession) -> Credentials:
    try:
        query = select(Users).join(Credentials, Users.id == Credentials.user_id).where(
            and_(
                Credentials.credential_type == CredentialTypes.BASIC,
                or_(
                    Users.email == identity,
                    Users.phone == identity
                )
            )
        )
        result = (await session.execute(query)).scalars().first()
        if not result:
            raise NotFoundException("User not found")
        return result
    except IntegrityError as e:
        raise InternalServerError(e) from e