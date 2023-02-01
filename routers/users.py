from fastapi import APIRouter, Depends, status, HTTPException
from dotenv import load_dotenv
from telethon.errors.rpcerrorlist import PhoneCodeExpiredError, FloodWaitError

from auth import auth
from schemas.users import Text
from schemas.telegram import TelegramLogin, TelegramSendCode, TelegramResponseCode
from schemas.settings import Settings
from utils.text import generate_random_string
from utils.telegram_client import get_telegram_client

load_dotenv()

settings = Settings()
router = APIRouter()


@router.post('/send-code', status_code=status.HTTP_201_CREATED, response_model=TelegramResponseCode)
async def send_authorizarion_code(request: TelegramSendCode, api_key = Depends(auth.get_user_api_key)):
    client = await get_telegram_client(settings)
    await client.connect()
    try:
        await client.send_code_request(request.phone_number)
    except FloodWaitError as ex:
        error = {
            'FloodWaitError': {
                'phone_number': ex.request.phone_number,
                'seconds': ex.seconds
            }}
        raise HTTPException(status.HTTP_400_BAD_REQUEST, error)
    result = {'session': client.session.save()}
    return result


@router.post('/login-telegram', status_code=status.HTTP_201_CREATED)
async def login_telegram(request: TelegramLogin, api_key = Depends(auth.get_user_api_key)):
    client = await get_telegram_client(settings, request.session)
    await client.connect()
    await client.send_code_request(request.phone_number)
    try:
        data = await client.sign_in(request.phone_number, request.phone_code)
    except PhoneCodeExpiredError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'The confirmation code has expired')
    return data.to_dict()


@router.get('/send-random-text', status_code=status.HTTP_200_OK, response_model=Text)
async def send_random_text(chat_id: int, limit_length: int = 10, api_key = Depends(auth.get_user_api_key)):
    client = await get_telegram_client(settings)
    await client.connect()
    random_text = await generate_random_string(string_length=limit_length)
    await client.send_message(chat_id, random_text)
    data = {'text': random_text}
    return data

