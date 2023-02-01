from fastapi import APIRouter, Depends, status
from fastapi.security.api_key import APIKey

from auth import auth
from schemas.users import ApiKey
from utils.text import generate_user_api_key

router = APIRouter()


@router.post('/create_apikey', status_code=status.HTTP_201_CREATED, response_model=ApiKey)
async def generate_apikey(api_key: APIKey = Depends(auth.get_admin_api_key)):
    user_api_key = await generate_user_api_key()
    data = {'api_key': user_api_key}
    return data