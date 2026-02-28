from sqlalchemy import Column, Integer, String, Boolean
from src.config.database import Base
from sqlalchemy.orm import relationship
from enum import Enum

class RoleEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_no = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default=RoleEnum.USER.value)
    is_active = Column(Boolean, default=True)

    orders = relationship("Order", back_populates="customer")
    def __repr__(self):
        return f"User is {self.username}"
