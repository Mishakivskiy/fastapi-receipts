from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=False, nullable=False)
    username: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)


class Receipt(Base):
    __tablename__ = "receipts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    total: Mapped[float] = mapped_column(Float)
    payment_type: Mapped[str] = mapped_column(String)
    payment_amount: Mapped[float] = mapped_column(Float)
    rest: Mapped[float] = mapped_column(Float)

    products = relationship("ReceiptProduct", back_populates="receipt")


class ReceiptProduct(Base):
    __tablename__ = "receipt_products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    receipt_id: Mapped[int] = mapped_column(Integer, ForeignKey("receipts.id"))
    name: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    quantity: Mapped[float] = mapped_column(Float)
    total: Mapped[float] = mapped_column(Float)

    receipt = relationship("Receipt", back_populates="products")