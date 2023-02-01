import os

import uvicorn
from fastapi import FastAPI

from routers import users, admins

app = FastAPI(title='FastAPI-Telegram')

app.include_router(users.router, tags=['User'])
app.include_router(admins.router, tags=['Admin'])


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT')))