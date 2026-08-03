import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.config import setting
from src.modules.hotels.models import HotelSearchHistory
from src.modules.places.models import Place

GEOCODE_URL = "https://api.geoapify.com/v1/geocode/search"
PLACES_URL = "https://api.geoapify.com/v2/places"


class HotelsService:
    def __init__(self):
        self.api_key = setting.PLACE_API

    async def search_hotels(self, place: str, user_id: int, db: Session) -> list:

        # Step 1: Reuse saved place data if available, otherwise geocode
        saved = db.query(Place).filter(
            Place.user_id == user_id,
            Place.name == place
        ).first()

        if saved and saved.latitude is not None and saved.longitude is not None:
            lat = float(saved.latitude)
            lon = float(saved.longitude)
        else:
            async with httpx.AsyncClient() as client:
                geo_resp = await client.get(
                    GEOCODE_URL,
                    params={
                        "text": place,
                        "format": "json",
                        "apiKey": self.api_key,
                    },
                )

            geo_data = geo_resp.json()

            if not geo_data.get("results"):
                raise HTTPException(
                    status_code=404,
                    detail=f"Location '{place}' not found."
                )

            location = geo_data["results"][0]
            lat = location["lat"]
            lon = location["lon"]

            # Auto-save the place so future searches skip geocoding
            db.add(Place(
                user_id=user_id,
                name=place,
                country=location.get("country"),
                state=location.get("state"),
                city=location.get("city"),
                latitude=lat,
                longitude=lon,
            ))
            db.commit()

        # Step 2: Search hotels
        async with httpx.AsyncClient() as client:
            places_resp = await client.get(
                PLACES_URL,
                params={
                    "categories": "accommodation.hotel",
                    "filter": f"circle:{lon},{lat},5000",
                    "limit": 20,
                    "apiKey": self.api_key,
                },
            )

        places_data = places_resp.json()

        hotels = []

        for feature in places_data.get("features", []):
            props = feature.get("properties", {})
            coords = feature.get("geometry", {}).get("coordinates", [None, None])

            hotels.append(
                {
                    "name": props.get("name", "Unknown"),
                    "address": props.get("formatted"),
                    "latitude": coords[1],
                    "longitude": coords[0],
                    "categories": props.get("categories", []),
                    "website": props.get("website"),
                    "phone": str(props.get("contact", {}).get("phone"))
                    if props.get("contact", {}).get("phone")
                    else None,
                }
            )

        # Save search history
        history = HotelSearchHistory(
            user_id=user_id,
            place=place,
        )

        db.add(history)
        db.commit()

        return hotels


hotels_service = HotelsService()