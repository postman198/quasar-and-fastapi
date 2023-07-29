import datetime as _dt
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    # if title filed is not unique ==> title = Column(String(100), unique=True, index=True)
    title = Column(String(100), index=True)
    description = Column(Text)
    status = Column(String, default="open")
    date_created = Column(DateTime, default=_dt.datetime.utcnow)

    owner = relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"<Task title={self.title} description={self.description} status={self.status}>"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    date_created = Column(DateTime, default=_dt.datetime.utcnow)

    tasks = relationship("Task", back_populates="owner")

