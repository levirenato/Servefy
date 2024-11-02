from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class OrderStatus(enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    completed = "completed"
    canceled = "canceled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)
    created_at = Column(DateTime, nullable=False)
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    order = relationship("Order", back_populates="items")
