from pydantic import BaseModel


class TelegramLogin(BaseModel):
    phone_number: str
    phone_code: int
    session: str


class TelegramSendCode(BaseModel):
    phone_number: str