from fastapi import APIRouter, Depends, status
from fastapi.security.api_key import APIKey
from sqlalchemy.ext.asyncio import AsyncSession

from auth import auth
from db.db import get_session
from schemas.users import ApiKey
from service.users import create_api_key

router = APIRouter()


@router.post('/create_apikey', status_code=status.HTTP_201_CREATED, response_model=ApiKey)
async def generate_apikey(session: AsyncSession = Depends(get_session), api_key: APIKey = Depends(auth.get_admin_api_key)):
    data = await create_api_key(session)
    return data