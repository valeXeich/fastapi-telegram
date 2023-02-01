from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE = 'postgresql+asyncpg://postgres:postgres@localhost/postgres'

engine = create_async_engine(DATABASE)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
session = async_session()

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

Base = declarative_base()