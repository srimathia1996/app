from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, Enum
from app.database.base import Base
import uuid
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    email = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Product(Base):
    __tablename__ = "products"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    price = Column(Float)
    stock_quantity = Column(Integer)


class Order(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    total_amount = Column(Float)
    tax_amount = Column(Float)
    shipping_amount = Column(Float)
    status = Column(String, default="PENDING")
    created_at = Column(DateTime, default=datetime.utcnow)


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(String, ForeignKey("orders.id"))
    product_id = Column(String, ForeignKey("products.id"))
    quantity = Column(Integer)
    price = Column(Float)


class Payment(Base):
    __tablename__ = "payments"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(String, ForeignKey("orders.id"))
    payment_gateway_id = Column(String)
    payment_status = Column(String)
    amount = Column(Float)
    currency = Column(String)
    idempotency_key = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)