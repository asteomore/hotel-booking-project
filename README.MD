# Hotel Booking Service

Простой сервис для управления номерами отелей и бронированиями на FastAPI + PostgreSQL.

## Запуск через Docker + Docker-Compose

1.  В корне проекта должен быть `.env` со строкой подключения к БД.
`DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/hotel_db`

    Для запуска тестов через IDE в переменную `Environment Variables` нужно вписать данную строку:
`DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/hotel_db`


2.  Запустить Docker-compose:
`docker-compose up --build`
3.  Сервис будет доступен по адресу:
`http://localhost:9000`

## Структура

1. Структура БД.

Таблицы создаются из `db/init.sql`:
    
`rooms`: id(PK), description(text), price(numeric), created_at(timestamp)

`bookings`: id(PK), room_id(FK -> rooms.id), date_start(date), date_end(date)

2. HTTP API

- Номера:

`POST /rooms/create` - создать номер

    Запрос (JSON): `{"description": "text", "price": 100.99}`
    Ответ: `{"room_id": 1}`

`DELETE /rooms/delete?room_id=1` - удалить номер и все его брони

    Успех: {"message": "room deleted"}
    Ошибка: {"detail": "room not found"}

`GET /rooms/list?sort_by=price&order=asc` - список номеров

    Параметры: sort_by=price|created_at, order=asc|desc
    Ответ: [{ "id": 1, "description": "...", "price": 100.99, "created_at": "..." }, ...]

- Бронирования:

`POST /bookings/create` - создать бронь (form-data)

    Поля: room_id, date_start=YYYY-MM-DD, date_end=YYYY-MM-DD
    Успех: {"booking_id": 1}
    Ошибки: {"detail": "date_end must be equal or after date_start"}
            {"detail": "room is already booked"}

`DELETE /bookings/delete?booking_id=1` - удалить бронь
    
    Успех: {"message": "booking deleted"}
    Ошибка: {"detail": "booking not found"}

`GET /bookings/list?room_id=1` - список броней номера

    Ответ: [{ "booking_id": 1, "date_start": "2025-12-05", "date_end": "2025-12-10" }, ...] (отсортированы по date_start)

## Технические детали

- Модели и схемы:
  - SQLAlchemy‑модели находятся в `src/hotel_booking/models.py`.
  - Pydantic‑схемы запросов/ответов - `src/hotel_booking/schemas.py`.
- Настройка БД:
  - Подключение и сессия SQLAlchemy - `src/hotel_booking/database.py`.
- HTTP‑хендлеры:
  - Эндпоинты для номеров и броней - `src/hotel_booking/api/v1/rooms.py` и `src/hotel_booking/api/v1/bookings.py`.
- Docker:
  - `Dockerfile` собирает образ приложения (Python 3.12-slim, установка зависимостей из `requirements.txt`).
  - `docker-compose.yml` поднимает два сервиса: `db` (PostgreSQL) и `app` (FastAPI).
- Тесты:
  - Общие фикстуры находятся в `tests/conftest.py`.
  - Основные API‑тесты - в `tests/test_api_v2.py`.


## Тесты

Делаются (при работающем PostgreSQL, как в docker-compose):

- создание номера и брони;
- удаление брони;
- удаление номера и удаление его броней;
- `404` для несуществующих номера/брони;
- сортировка `/rooms/list` по цене и дате добавления;
- проверка на пересекающиеся брони;
- запрет брони, если `date_end < date_start`.
