from decimal import Decimal


def test_create_room_and_booking(api_client, room_id, booking_id):
    result = api_client.get(f"/bookings/list?room_id={room_id}")
    assert result.status_code == 200
    data = result.json()
    assert len(data) == 1
    assert data[0]["booking_id"] == booking_id
    assert data[0]["date_start"] == "2025-12-05"
    assert data[0]["date_end"] == "2025-12-10"


def test_delete_booking(clear_db, api_client, room_id, booking_id):
    delete_booking = api_client.delete(f"/bookings/delete?booking_id={booking_id}")
    assert delete_booking.status_code == 200
    assert delete_booking.json() == {"message": "booking deleted"}

    get_booking = api_client.get(f"/bookings/list?room_id={room_id}")
    assert get_booking.status_code == 200
    data = get_booking.json()
    assert len(data) == 0


def test_delete_room_and_also_booking(clear_db, api_client, room_id, booking_id):
    delete_room = api_client.delete(f"/rooms/delete?room_id={room_id}")
    assert delete_room.status_code == 200
    assert delete_room.json() == {"message": "room deleted"}

    get_room = api_client.get("/rooms/list")
    assert get_room.status_code == 200
    rooms = get_room.json()
    for room in rooms:
        assert room["id"] != room_id
    get_booking = api_client.get(f"/bookings/list?room_id={room_id}")
    assert get_booking.status_code == 200
    data = get_booking.json()
    assert len(data) == 0


def test_delete_not_existent_room(clear_db, api_client):
    delete_room = api_client.delete("/rooms/delete", params={"room_id": 9999})
    assert delete_room.status_code == 404
    assert delete_room.json() == {"detail": "room not found"}


def test_delete_not_existent_booking(clear_db, api_client):
    delete_booking = api_client.delete("/bookings/delete", params={"booking_id": 9999})
    assert delete_booking.status_code == 404
    assert delete_booking.json() == {"detail": "booking not found"}


def test_rooms_sorted_by_price_asc(clear_db, api_client):
    test_room1 = api_client.post(
        "/rooms/create", json={"description": "test room", "price": 500}
    )
    assert test_room1.status_code == 200
    test_room2 = api_client.post(
        "/rooms/create", json={"description": "test room", "price": 1000}
    )
    assert test_room2.status_code == 200
    test_room3 = api_client.post(
        "/rooms/create", json={"description": "test room", "price": 500.99}
    )
    assert test_room3.status_code == 200
    test_room4 = api_client.post(
        "/rooms/create", json={"description": "test room", "price": 501}
    )
    assert test_room4.status_code == 200
    get_room = api_client.get(
        "/rooms/list", params={"sort_by": "price", "order": "asc"}
    )
    assert get_room.status_code == 200
    rooms = get_room.json()
    prices = []
    for room in rooms:
        prices.append(Decimal(room["price"]))
    assert prices == sorted(prices)


def test_rooms_sorted_by_price_desc(clear_db, api_client):
    test_room1 = api_client.post(
        "/rooms/create", json={"description": "test room", "price": 500}
    )
    assert test_room1.status_code == 200
    test_room2 = api_client.post(
        "/rooms/create", json={"description": "test room", "price": 1000}
    )
    assert test_room2.status_code == 200
    test_room3 = api_client.post(
        "/rooms/create", json={"description": "test room", "price": 500.99}
    )
    assert test_room3.status_code == 200
    test_room4 = api_client.post(
        "/rooms/create", json={"description": "test room", "price": 501}
    )
    assert test_room4.status_code == 200
    get_room = api_client.get(
        "/rooms/list", params={"sort_by": "price", "order": "desc"}
    )
    assert get_room.status_code == 200
    rooms = get_room.json()
    prices = []
    for room in rooms:
        prices.append(Decimal(room["price"]))
    assert prices == sorted(prices, reverse=True)


def test_rooms_sorted_by_created_date_asc(clear_db, api_client):
    test_room1 = api_client.post(
        "/rooms/create", json={"description": "test room", "price": 500}
    )
    assert test_room1.status_code == 200
    test_room2 = api_client.post(
        "/rooms/create", json={"description": "test room", "price": 1000}
    )
    assert test_room2.status_code == 200
    test_room3 = api_client.post(
        "/rooms/create", json={"description": "test room", "price": 200}
    )
    assert test_room3.status_code == 200
    test_room4 = api_client.post(
        "/rooms/create", json={"description": "test room", "price": 10}
    )
    assert test_room4.status_code == 200
    get_room = api_client.get(
        "/rooms/list", params={"sort_by": "created_at", "order": "asc"}
    )
    assert get_room.status_code == 200
    rooms = get_room.json()
    dates = []
    for room in rooms:
        dates.append(room["created_at"])
    assert dates == sorted(dates)


def test_rooms_sorted_by_created_date_desc(clear_db, api_client):
    test_room1 = api_client.post(
        "/rooms/create", json={"description": "test room", "price": 500}
    )
    assert test_room1.status_code == 200
    test_room2 = api_client.post(
        "/rooms/create", json={"description": "test room", "price": 1000}
    )
    assert test_room2.status_code == 200
    test_room3 = api_client.post(
        "/rooms/create", json={"description": "test room", "price": 200}
    )
    assert test_room3.status_code == 200
    test_room4 = api_client.post(
        "/rooms/create", json={"description": "test room", "price": 10}
    )
    assert test_room4.status_code == 200
    get_room = api_client.get(
        "/rooms/list", params={"sort_by": "created_at", "order": "desc"}
    )
    assert get_room.status_code == 200
    rooms = get_room.json()
    dates = []
    for room in rooms:
        dates.append(room["created_at"])
    assert dates == sorted(dates, reverse=True)


def test_post_overbooked(clear_db, api_client, room_id):
    test_booking1 = api_client.post(
        "/bookings/create",
        data={
            "room_id": room_id,
            "date_start": "2025-12-05",
            "date_end": "2025-12-10",
        },
    )
    assert test_booking1.status_code == 200

    test_booking2 = api_client.post(
        "/bookings/create",
        data={
            "room_id": room_id,
            "date_start": "2025-12-08",
            "date_end": "2025-12-12",
        },
    )
    assert test_booking2.status_code == 400
    assert test_booking2.json() == {"detail": "room is already booked"}


def test_booking_invalid_dates(clear_db, api_client, room_id):
    resp = api_client.post(
        "/bookings/create",
        data={
            "room_id": room_id,
            "date_start": "2025-12-10",
            "date_end": "2025-12-05",
        },
    )
    assert resp.status_code == 400
    assert resp.json() == {"detail": "date_end must be equal or after date_start"}
