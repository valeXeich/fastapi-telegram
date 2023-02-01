from pydantic import BaseModel


class Text(BaseModel):
    text: str


class TelegramVerify(BaseModel):
    phone_number: str
    phone_code: str
    phone_hash: str


class ApiKey(BaseModel):
    api_key: str