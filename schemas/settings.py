import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    admin_api_key: str = os.getenv('ADMIN_API_KEY')
    bot_api_id: int = os.getenv('BOT_API_ID')
    bot_api_hash: str = os.getenv('BOT_API_HASH')