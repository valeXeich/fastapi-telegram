import os

from fastapi.security.api_key import APIKeyHeader
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Security, HTTPException, status
from starlette.status import HTTP_403_FORBIDDEN


admin_api_key = APIKeyHeader(name="apikey", auto_error=False)
user_api_key = HTTPBearer()


async def get_admin_api_key(api_key_header: str = Security(admin_api_key)):
    if api_key_header == '123':
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate ADMIN API KEY"
        )


async def get_user_api_key(api_key_header: HTTPAuthorizationCredentials = Security(user_api_key)):
    if api_key_header.credentials == '1234':
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
        )

