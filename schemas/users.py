from pydantic import BaseModel


class TextLimit(BaseModel):
    text_length: int


class TelegramVerify(BaseModel):
    phone_number: str
    phone_code: str
    phone_hash: str