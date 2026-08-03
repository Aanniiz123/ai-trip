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
def hotel_search(request):
    """Standalone hotel search page."""
    headers = get_auth_headers(request)
    hotels = []
    error = None
    place = ""
    if request.method == "POST":
        place = request.POST.get("place", "")
        try:
            resp = requests.post(
                f"{API_BASE}/hotels/search",
                json={"place": place},
                timeout=10,
                headers=headers,
            )
            resp.raise_for_status()
            hotels = resp.json()
        except requests.exceptions.HTTPError as e:
            try:
                error = e.response.json().get("detail", str(e))
            except Exception:
                error = str(e)
        except Exception as e:
            error = str(e)
    return render(request, "hotels/hotel_search.html", {"hotels": hotels, "error": error, "place": place})


@login_required_session
def hotel_history(request):
    """Show hotel search history for the logged-in user."""
    headers = get_auth_headers(request)
    try:
        resp = requests.get(f"{API_BASE}/hotels/history", timeout=5, headers=headers)
        resp.raise_for_status()
        history = resp.json()
    except Exception as e:
        history = []
        error = str(e)
    else:
        error = None
    return render(request, "hotels/hotel_history.html", {"history": history, "error": error})
