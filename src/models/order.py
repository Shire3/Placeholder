from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database import Base
from enum import Enum

class DeliveryStatus(str, Enum):
    PENDING = "pending"
    IS_DELIVERING = "is_delivering"
    DELIVERED = "delivered"



class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    size = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False, default = 1)
    price = Column(Float, nullable=False)
    pizza_type = Column(String, nullable=False)
    toppings = Column(Float)
    order_status = Column(String, default= DeliveryStatus.PENDING)
    user_id= Column(Integer, ForeignKey("users.id"), nullable = False)

    customer= relationship("User", back_populates="orders")