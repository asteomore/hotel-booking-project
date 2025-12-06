from fastapi import APIRouter, HTTPException, Form
from datetime import date

from src.database import SessionLocal
from src.models import Booking
from src.schemas import BookingOut

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.get("/list", response_model=list[BookingOut])
def get_bookings(room_id: int) -> list[BookingOut]:
    db = SessionLocal()
    try:
        bookings = (
            db.query(Booking)
            .filter(Booking.room_id == room_id)
            .order_by(Booking.date_start.asc())
            .all()
        )
        return [
            BookingOut(
                booking_id = b.id,
                date_start = b.date_start,
                date_end = b.date_end,
            )
            for b in bookings
        ]
    finally:
        db.close()

@router.post("/create")
def post_booking(
    room_id: int = Form(...),
    date_start: date = Form(...),
    date_end: date = Form(...),
) -> dict[str, int]:
    if date_end < date_start:
        raise HTTPException(status_code=400, detail="date_end must be equal or after date_start")

    db = SessionLocal()
    try:
        bookings = (
            db.query(Booking)
            .filter(Booking.room_id == room_id)
            .order_by(Booking.date_start.asc())
            .all()
        )
        for booking in bookings:
            overbooked: bool = not (date_end < booking.date_start or date_start > booking.date_end)
            if overbooked:
                raise HTTPException(status_code=400, detail="room is already booked")

        db_booking = Booking(
            room_id=room_id,
            date_start=date_start,
            date_end=date_end,
        )
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)
        return {"booking_id": db_booking.id}
    finally:
        db.close()



@router.delete("/delete")
def delete_booking(booking_id: int) -> dict[str, str]:
    db = SessionLocal()
    try:
        db_booking = db.query(Booking).filter(Booking.id == booking_id).first()
        if db_booking is not None:
            db.delete(db_booking)
            db.commit()
            return {"message": "booking deleted"}
        else:
            raise HTTPException(status_code=404, detail="booking not found")
    finally:
        db.close()