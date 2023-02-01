from pydantic import BaseModel


class TelegramLogin(BaseModel):
    phone_number: str
    phone_code: int
    session: str


class TelegramResponseCode(BaseModel):
    message: str = 'send'
    session: str


class TelegramSendCode(BaseModel):
    phone_number: str


class SendMessage(BaseModel):
    text_length: int = 10
    chat_id: int