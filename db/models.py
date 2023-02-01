from sqlalchemy import Column, Integer

from .db import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    api_key = Column(Integer, unique=True, nullable=False)