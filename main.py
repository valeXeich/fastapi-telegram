import os

import uvicorn
from fastapi import FastAPI

from routers import users, admins
from utils.db import init_models

app = FastAPI(title='FastAPI-Telegram')

app.include_router(users.router, tags=['User'])
app.include_router(admins.router, tags=['Admin'])


@app.on_event('startup')
async def startup():
    await init_models()


# if __name__ == '__main__':
#     uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT')))