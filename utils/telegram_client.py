from telethon import TelegramClient


async def get_telegram_client(settings, session: str = 'session') -> TelegramClient:
    return TelegramClient(
        session,
        api_id=settings.bot_api_id,
        api_hash=settings.bot_api_hash
    )