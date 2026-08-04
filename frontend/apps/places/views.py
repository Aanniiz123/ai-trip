from django.shortcuts import render, redirect
import requests
from django.conf import settings

API_BASE = getattr(settings, "API_BASE_URL", "http://127.0.0.1:8000")


def login_required_session(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get("access_token"):
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return wrapper


def get_auth_headers(request):
    token = request.session.get("access_token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


@login_required_session
def place_search(request):
    """Search for a city/place and save it to the user's list."""
    headers = get_auth_headers(request)
    result = None
    error = None
    city = ""

    if request.method == "POST":
        city = request.POST.get("city", "").strip()
        try:
            resp = requests.post(
                f"{API_BASE}/places/search",
                json={"city": city},
                timeout=10,
                headers=headers,
            )
            resp.raise_for_status()
            result = resp.json()
        except requests.exceptions.HTTPError as e:
            try:
                error = e.response.json().get("detail", str(e))
            except Exception:
                error = str(e)
        except Exception as e:
            error = str(e)

    return render(request, "places/place_search.html", {
        "result": result,
        "error": error,
        "city": city,
    })


@login_required_session
def place_list(request):
    """List all saved places for the logged-in user."""
    headers = get_auth_headers(request)
    try:
        resp = requests.get(f"{API_BASE}/places/", timeout=5, headers=headers)
        resp.raise_for_status()
        places = resp.json()
    except Exception as e:
        places = []
        error = str(e)
    else:
        error = None
    return render(request, "places/place_list.html", {"places": places, "error": error})


@login_required_session
def place_delete(request, place_id):
    """Delete a saved place."""
    headers = get_auth_headers(request)
    if request.method == "POST":
        try:
            resp = requests.delete(
                f"{API_BASE}/places/{place_id}",
                timeout=5,
                headers=headers,
            )
            resp.raise_for_status()
        except Exception:
            pass
    return redirect("place-list")
