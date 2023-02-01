from fastapi import APIRouter, Depends
from fastapi.security.api_key import APIKey
from fastapi.security import HTTPAuthorizationCredentials
from dotenv import load_dotenv

from auth import auth
from utils.text import generate_random_string



router = APIRouter()


@router.post('/test1')
async def verify_telegram():
    ...


@router.get('/test')
async def get_random_text(api_key: HTTPAuthorizationCredentials = Depends(auth.get_user_api_key)):
    ...


@router.post('/create_apikey')
async def generate_apikey(api_key: APIKey = Depends(auth.get_admin_api_key)):
    user_api_key = generate_random_string()
    return user_api_key
