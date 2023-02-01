from fastapi import APIRouter
from dotenv import load_dotenv



router = APIRouter()


@router.post()
async def verify_telegram():
    ...


@router.get()
async def get_random_text():
    ...


@router.posh()
async def generate_apikey():
    ...
