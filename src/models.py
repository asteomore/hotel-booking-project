from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.sql import func

from src.database import Base


class Room(Base):
    __tablename__ = "rooms"

    id: int = Column(Integer, primary_key=True, index=True)
    description: str = Column(String(255), nullable=False)
    price: Decimal = Column(Numeric(10, 2), nullable=False)
    created_at: datetime = Column(DateTime, nullable=False, server_default=func.now())


class Booking(Base):
    __tablename__ = "bookings"

    id: int = Column(Integer, primary_key=True, index=True)
    date_start: date = Column(Date, nullable=False)
    date_end: date = Column(Date, nullable=False)
    room_id: int = Column(Integer, ForeignKey("rooms.id"), nullable=False)
