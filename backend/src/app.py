from fastapi import FastAPI
# from src.routers import trips, auth, place_router
from src.modules.auth import router as auth_module
from src.modules.trips import router as trips_module
from src.modules.places import router as places_module
from src.modules.users import router as users_module

app = FastAPI(title="Trip Planner API")

@app.get("/health")
def health_check():
    return {"status": "ok"}

# app.include_router(trips.router)
# app.include_router(auth.router)
# app.include_router(place_router.router)

app.include_router(auth_module.router, prefix="/v2")
app.include_router(trips_module.router, prefix="/v2")
app.include_router(places_module.router, prefix="/v2")
app.include_router(users_module.router, prefix="/v2")
