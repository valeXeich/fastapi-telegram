import secrets
import random
import string


async def generate_random_string(string_length: int = 20):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(string_length))


async def generate_user_api_key():
    api_key = secrets.token_urlsafe(16)
    return api_key
