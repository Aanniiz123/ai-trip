from fastapi import FastAPI

from src.modules.auth import router as auth_module
from src.modules.trips import router as trips_module
from src.modules.places import router as places_module
from src.modules.users import router as users_module
from src.modules.hotels.router import router as hotels_router
from src.modules.chat.router import router as chat_router

app = FastAPI(title="Trip Planner API")



app.include_router(auth_module.router, prefix="/v2")
app.include_router(trips_module.router, prefix="/v2")
app.include_router(places_module.router, prefix="/v2")
app.include_router(users_module.router, prefix="/v2")
app.include_router(hotels_router, prefix="/v2")
app.include_router(chat_router, prefix="/v2")
