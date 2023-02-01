from fastapi import APIRouter, Depends, status, HTTPException
from telethon.errors.rpcerrorlist import PhoneCodeExpiredError, FloodWaitError, AuthKeyUnregisteredError, ApiIdInvalidError

from auth import auth
from config import settings
from schemas.users import Text
from schemas.telegram import TelegramLogin, TelegramSendCode, TelegramResponseCode, SendMessage
from utils.text import generate_random_string
from utils.telegram_client import get_telegram_client


router = APIRouter()


@router.post('/send-code', status_code=status.HTTP_201_CREATED, response_model=TelegramResponseCode)
async def send_authorizarion_code(request: TelegramSendCode, api_key = Depends(auth.get_user_api_key)):
    try:
        client = await get_telegram_client(settings)
        await client.connect()
        await client.send_code_request(request.phone_number)
    except FloodWaitError as ex:
        error = {
            'FloodWaitError': {
                'phone_number': ex.request.phone_number,
                'seconds': ex.seconds
            }}
        raise HTTPException(status.HTTP_400_BAD_REQUEST, error)
    except ApiIdInvalidError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Invalid API_ID OR API_HASH')
    result = {'session': client.session.save()}
    return result


@router.post('/login-telegram', status_code=status.HTTP_201_CREATED)
async def login_telegram(request: TelegramLogin, api_key = Depends(auth.get_user_api_key)):
    try:
        client = await get_telegram_client(settings, request.session)
        await client.connect()
        await client.send_code_request(request.phone_number)
        data = await client.sign_in(request.phone_number, request.phone_code)
    except PhoneCodeExpiredError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'The confirmation code has expired')
    except ApiIdInvalidError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Invalid API_ID OR API_HASH')
    return data.to_dict()


@router.post('/send-random-text', status_code=status.HTTP_201_CREATED, response_model=Text)
async def send_random_text(request: SendMessage, api_key = Depends(auth.get_user_api_key)):
    try:
        client = await get_telegram_client(settings)
        await client.connect()
        random_text = await generate_random_string(string_length=request.text_length)
        await client.send_message(request.chat_id, random_text)
        data = {'text': random_text}
    except AuthKeyUnregisteredError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'The key is not registered in the system')
    return data

