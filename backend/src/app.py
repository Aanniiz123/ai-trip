from fastapi import FastAPI
from src.routers import trips, auth



app = FastAPI(title="Trip Planner API")

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(trips.router)
app.include_router(auth.router)
