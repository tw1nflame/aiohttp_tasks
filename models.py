from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from db import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    is_done = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    deadline = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True),
                        onupdate=func.now(), server_default=func.now())
