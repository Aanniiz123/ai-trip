
import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.config import setting
from src.modules.places.models import Place
from src.modules.places.schemas import PlaceCreate

API_KEY = setting.PLACE_API
GEOCODE_URL = "https://api.geoapify.com/v1/geocode/search"


class PlacesService:
    def __init__(self):
        self.api_key = API_KEY
        self.geocode_url = GEOCODE_URL

    async def search_city(self, city: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.geocode_url,
                params={
                    "text": city,
                    "format": "json",
                    "apiKey": self.api_key
                }
            )
        data = response.json()

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=data)

        if "results" not in data or len(data["results"]) == 0:
            return {
                "success": False,
                "message": f"No location found for '{city}'."
            }

        location = data["results"][0]

        return {
            "success": True,
            "searched": city,
            "country": location.get("country"),
            "state": location.get("state"),
            "city": location.get("city"),
            "latitude": location.get("lat"),
            "longitude": location.get("lon")
        }


places_service = PlacesService()


def create_place(db: Session, user_id: int, place_data: PlaceCreate) -> Place:
    place = Place(
        user_id=user_id,
        trip_id=place_data.trip_id,
        name=place_data.name,
        country=place_data.country,
        state=place_data.state,
        city=place_data.city,
        latitude=place_data.latitude,
        longitude=place_data.longitude,
    )
    db.add(place)
    db.commit()
    db.refresh(place)
    return place
