from fastapi import FastAPI
from src.api.rooms import router as rooms_router
from src.api.bookings import router as booking_router

app = FastAPI()

app.include_router(rooms_router)
app.include_router(booking_router)

