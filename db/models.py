from sqlalchemy import Column, Integer, String

from .db import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    api_key = Column(String, unique=True, nullable=False)