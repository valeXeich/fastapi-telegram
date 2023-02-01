from fastapi import FastAPI

from routers import users, admins

app = FastAPI(title='FastAPI-Telegram')

app.include_router(users.router, tags=['User'])
app.include_router(admins.router, tags=['Admin'])