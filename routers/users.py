from fastapi import APIRouter, Depends, status
from fastapi.security.api_key import APIKey

from auth import auth
from schemas.users import TelegramVerify
from utils.text import generate_random_string, generate_user_api_key



router = APIRouter()


@router.post('/test1')
async def verify_telegram(request: TelegramVerify, api_key = Depends(auth.get_user_api_key)):
    ...


@router.get('/get-random-text', status_code=status.HTTP_200_OK)
async def get_random_text(limit_length: int = 10, api_key = Depends(auth.get_user_api_key)):
    random_text = await generate_random_string(string_length=limit_length)
    return random_text


@router.post('/create_apikey')
async def generate_apikey(api_key: APIKey = Depends(auth.get_admin_api_key)):
    user_api_key = await generate_user_api_key()
    return {'api_key': user_api_key}
