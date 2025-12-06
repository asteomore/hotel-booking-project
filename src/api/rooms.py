from fastapi import APIRouter, HTTPException

from src.database import SessionLocal
from src.models import Booking, Room
from src.schemas import RoomCreate, RoomOut

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.get("/list", response_model=list[RoomOut])
def get_rooms(sort_by: str | None = None, order: str | None = None) -> list[RoomOut]:
    db = SessionLocal()
    try:
        query = db.query(Room)
        if sort_by == "price" and order == "asc":
            query = query.order_by(Room.price.asc())
        elif sort_by == "price" and order == "desc":
            query = query.order_by(Room.price.desc())
        elif sort_by == "created_at" and order == "asc":
            query = query.order_by(Room.created_at.asc())
        else:
            query = query.order_by(Room.created_at.desc())

        rooms = query.all()
        return [
            RoomOut(
                id=room.id,
                description=room.description,
                price=room.price,
                created_at=room.created_at,
            )
            for room in rooms
        ]
    finally:
        db.close()


@router.post("/create")
def post_rooms(room: RoomCreate) -> dict[str, int]:
    db = SessionLocal()
    try:
        db_room = Room(
            description=room.description,
            price=room.price,
        )
        db.add(db_room)
        db.commit()
        db.refresh(db_room)
        return {"room_id": db_room.id}
    finally:
        db.close()


@router.delete("/delete")
def delete_rooms(room_id: int) -> dict[str, str]:
    db = SessionLocal()
    try:
        db_room = db.query(Room).filter(Room.id == room_id).first()
        if db_room is not None:
            db.query(Booking).filter(Booking.room_id == room_id).delete()
            db.delete(db_room)
            db.commit()
            return {"message": "room deleted"}
        else:
            raise HTTPException(status_code=404, detail="room not found")
    finally:
        db.close()
