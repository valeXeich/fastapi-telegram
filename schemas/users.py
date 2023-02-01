from pydantic import BaseModel


class Text(BaseModel):
    text: str


class ApiKey(BaseModel):
    api_key: str