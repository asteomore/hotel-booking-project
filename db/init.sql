CREATE TABLE Rooms
(
    id SERIAL PRIMARY KEY,
    description VARCHAR(255) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Bookings
(
    id SERIAL PRIMARY KEY,
    room_id INT NOT NULL,
    date_start DATE NOT NULL,
    date_end DATE NOT NULL,
    FOREIGN KEY (room_id) REFERENCES Rooms(id)
);