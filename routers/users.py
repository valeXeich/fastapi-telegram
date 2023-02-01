from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.api_key import APIKey
from dotenv import load_dotenv
from telethon import TelegramClient, sync
from telethon.errors.rpcerrorlist import PhoneCodeExpiredError, FloodWaitError

from auth import auth
from schemas.users import ApiKey, Text
from schemas.telegram import TelegramLogin, TelegramSendCode
from schemas.settings import Settings
from utils.text import generate_random_string, generate_user_api_key
from utils.telegram_client import get_telegram_client

load_dotenv()

settings = Settings()
router = APIRouter()
client = TelegramClient('session', settings.bot_api_id, settings.bot_api_hash)


@router.post('/code')
async def send_authorizarion_code(request: TelegramSendCode):
    client = await get_telegram_client(settings)
    await client.connect()
    try:
        await client.send_code_request(request.phone_number)
    except FloodWaitError as ex:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, ex)
    return {
            'msg': 'code sent',
            'session': client.session.save()
        }


@router.post('/login-telegram')
async def verify_telegram(request: TelegramLogin, api_key = Depends(auth.get_user_api_key)):
    client = await get_telegram_client(settings, request.session)
    await client.connect()
    await client.send_code_request(request.phone_number)
    try:
        data = await client.sign_in(request.phone_number, request.phone_code)
    except PhoneCodeExpiredError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'The confirmation code has expired')
    except Exception as ex:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, ex)
    return data.to_dict()


@router.get('/get-random-text', status_code=status.HTTP_200_OK, response_model=Text)
async def get_random_text(limit_length: int = 10, api_key = Depends(auth.get_user_api_key)):
    random_text = await generate_random_string(string_length=limit_length)
    data = {'text': random_text}
    return data


@router.post('/create_apikey', status_code=status.HTTP_201_CREATED, response_model=ApiKey)
async def generate_apikey(api_key: APIKey = Depends(auth.get_admin_api_key)):
    user_api_key = await generate_user_api_key()
    data = {'api_key': user_api_key}
    return data
