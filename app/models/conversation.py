from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from sqlalchemy import Column, Integer, String

from app.database.database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)