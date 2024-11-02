from sqlalchemy import Column, DateTime, Float, Integer, String, Enum
from enum import Enum as PyEnum

from app.database import Base


class UserTypeEnum(PyEnum):
    customer = "customer"
    restaurant = "restaurant"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    birthday = Column(DateTime, nullable=False)
    user_type = Column(Enum(UserTypeEnum), nullable=False)
    hashed_password = Column(String, nullable=False)


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    event = Column(String, index=True)
    username = Column(String, index=True)
    timestamp = Column(Float)
