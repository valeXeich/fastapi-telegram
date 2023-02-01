from fastapi.security.api_key import APIKeyHeader
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Security, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from service.users import get_api_keys
from db.db import get_session


admin_api_key = APIKeyHeader(name="Authorization-Admin", auto_error=False)
user_api_key = HTTPBearer()


async def get_admin_api_key(api_key_header: str = Security(admin_api_key)):
    if api_key_header == settings.admin_api_key:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate ADMIN API KEY"
        )


async def get_user_api_key(api_key_header: HTTPAuthorizationCredentials = Security(user_api_key), session: AsyncSession = Depends(get_session)):
    api_keys = await get_api_keys(session)
    if api_key_header.credentials in api_keys:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
        )


