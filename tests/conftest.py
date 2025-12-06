from fastapi.testclient import TestClient
from src.main import app
import pytest
from src.database import SessionLocal
from src.models import Room, Booking


@pytest.fixture(autouse=True)
def clear_db():
    db = SessionLocal()
    try:
        db.query(Booking).delete()
        db.query(Room).delete()
        db.commit()
    finally:
        db.close()


@pytest.fixture()
def api_client():
    return TestClient(app)


@pytest.fixture()
def room_id(api_client):
    test_room = api_client.post(
        "/rooms/create", json={"description": "test room", "price": "100.99"}
    )
    assert test_room.status_code == 200
    return test_room.json()["room_id"]


@pytest.fixture()
def booking_id(api_client, room_id):
    test_booking = api_client.post(
        "/bookings/create",
        data={"room_id": room_id, "date_start": "2025-12-05", "date_end": "2025-12-10"},
    )
    assert test_booking.status_code == 200
    return test_booking.json()["booking_id"]
