from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel

# не используется, т.к. запрос идет через курл form-данные,
# а не JSON
# class BookingCreate(BaseModel):
#     room_id: int
#     date_start: date
#     date_end: date


class BookingOut(BaseModel):
    booking_id: int
    date_start: date
    date_end: date


class RoomCreate(BaseModel):
    description: str
    price: Decimal


class RoomOut(BaseModel):
    id: int
    description: str
    price: Decimal
    created_at: datetime
