from sqlalchemy import Integer, String, Column, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from .db import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)

    credit = relationship("Credit", back_populates="user", uselist=False, cascade="all, delete-orphan")


class Credit(Base):
    __tablename__ = "credits"

    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    credits = Column(Integer, nullable=False, default=0)
    last_updated = Column(TIMESTAMP(timezone=False), nullable=False, server_default=func.now())

    user = relationship("User", back_populates="credit")
