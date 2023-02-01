from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from utils.text import generate_user_api_key


async def create_api_key(session: AsyncSession):
    user_api_key = await generate_user_api_key()
    user = User(api_key=user_api_key)
    session.add(user)
    await session.commit()
    result = {'api_key': user_api_key}
    return result


async def get_api_keys(session: AsyncSession):
    query = select(User.api_key).select_from(User)
    result = await session.execute(query)
    return result.scalars().all()