from django.shortcuts import render, redirect
import requests
from django.conf import settings

# Create your views here.

API_BASE = getattr(settings, "API_BASE_URL", "http://127.0.0.1:8000")

def trip_list(request):
    """Fetch all the trips from the FastAPI backend and render them."""

    try:
        resp = requests.get(f"{API_BASE}/trips/", timeout=5)
        resp.raise_for_status()
        trips = resp.json()

    except Exception as e:
        trips = []
        error = str(e)

    else:
        error = None
    return render(request, "dashboard/trip_list.html", {"trips": trips, "error": error})



def trip_create(request):
    """Handle POST from the form to create a new trip."""
    if request.method == "POST":
        payload = {
            "title": request.POST.get("title"),
            "destination": request.POST.get("destination"),
            "start_date": request.POST.get("start_date"),
            "end_date": request.POST.get("end_date"),
        }
        try:
            resp = requests.post(f"{API_BASE}/trips/", json=payload, timeout=5)
            resp.raise_for_status()
        except Exception as e:
            error = str(e)
        else:
            error = None
        if error is None:
            return redirect("trip-list")
        # If there was an error, re-render the form with error message
        return render(request, "dashboard/trip_form.html", {"error": error})
    # GET – show the form
    return render(request, "dashboard/trip_form.html")

