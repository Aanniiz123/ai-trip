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
def trip_list(request):
    headers = get_auth_headers(request)
    try:
        resp = requests.get(f"{API_BASE}/trips/", timeout=5, headers=headers)
        resp.raise_for_status()
        trips = resp.json()
    except Exception as e:
        trips = []
        error = str(e)
    else:
        error = None
    return render(request, "dashboard/trip_list.html", {"trips": trips, "error": error})


@login_required_session
def trip_create(request):
    headers = get_auth_headers(request)
    if request.method == "POST":
        payload = {
            "title": request.POST.get("title"),
            "destination": request.POST.get("destination"),
            "start_date": request.POST.get("start_date"),
            "end_date": request.POST.get("end_date"),
            "trip_type": request.POST.get("trip_type", "solo"),
            "num_people": int(request.POST.get("num_people", 1)),
            "budget": float(request.POST.get("budget")) if request.POST.get("budget") else None,
            "currency": request.POST.get("currency", "USD"),
            "audience": request.POST.get("audience", "foreign"),
        }
        try:
            resp = requests.post(f"{API_BASE}/trips/", json=payload, timeout=5, headers=headers)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            try:
                error = e.response.json().get("detail", str(e))
            except Exception:
                error = str(e)
            return render(request, "dashboard/trip_form.html", {"error": error})
        except Exception as e:
            return render(request, "dashboard/trip_form.html", {"error": str(e)})
        return redirect("trip-list")
    return render(request, "dashboard/trip_form.html")


@login_required_session
def trip_detail(request, trip_id):
    headers = get_auth_headers(request)
    try:
        resp = requests.get(f"{API_BASE}/trips/{trip_id}", timeout=5, headers=headers)
        resp.raise_for_status()
        trip = resp.json()
        error = None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return render(request, "dashboard/trip_not_found.html", status=404)
        trip = None
        error = str(e)
    except Exception as e:
        trip = None
        error = str(e)

    # Fetch hotels for this trip's destination
    hotels = []
    hotels_error = None
    if trip:
        try:
            h_resp = requests.post(
                f"{API_BASE}/hotels/search",
                json={"place": trip["destination"]},
                timeout=10,
                headers=headers,
            )
            h_resp.raise_for_status()
            hotels = h_resp.json()
        except Exception as e:
            hotels_error = str(e)

    return render(request, "dashboard/trip_detail.html", {
        "trip": trip,
        "error": error,
        "hotels": hotels,
        "hotels_error": hotels_error,
    })


@login_required_session
def trip_edit(request, trip_id):
    headers = get_auth_headers(request)
    if request.method == "POST":
        payload = {
            "title": request.POST.get("title"),
            "destination": request.POST.get("destination"),
            "start_date": request.POST.get("start_date"),
            "end_date": request.POST.get("end_date"),
            "trip_type": request.POST.get("trip_type", "solo"),
            "num_people": int(request.POST.get("num_people", 1)),
            "budget": float(request.POST.get("budget")) if request.POST.get("budget") else None,
            "currency": request.POST.get("currency", "USD"),
            "audience": request.POST.get("audience", "foreign"),
        }
        try:
            resp = requests.put(f"{API_BASE}/trips/{trip_id}", json=payload, timeout=5, headers=headers)
            resp.raise_for_status()
            return redirect("trip-detail", trip_id=trip_id)
        except requests.exceptions.HTTPError as e:
            try:
                error = e.response.json().get("detail", str(e))
            except Exception:
                error = str(e)
        except Exception as e:
            error = str(e)
        return render(request, "dashboard/trip_form.html", {
            "error": error, "trip": payload, "is_edit": True, "trip_id": trip_id
        })

    try:
        resp = requests.get(f"{API_BASE}/trips/{trip_id}", timeout=5, headers=headers)
        resp.raise_for_status()
        trip = resp.json()
    except Exception as e:
        return render(request, "dashboard/trip_form.html", {"error": str(e)})
    return render(request, "dashboard/trip_form.html", {
        "trip": trip, "is_edit": True, "trip_id": trip_id
    })


@login_required_session
def trip_delete(request, trip_id):
    headers = get_auth_headers(request)

    if request.method == "POST":
        try:
            resp = requests.delete(f"{API_BASE}/trips/{trip_id}", timeout=5, headers=headers)
            resp.raise_for_status()
            return redirect("trip-list")
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response is not None else "?"
            try:
                body = e.response.json().get("detail", "") if e.response is not None else ""
            except Exception:
                body = e.response.text if e.response is not None else ""
            error = f"Delete failed (HTTP {status_code}): {body or str(e)}"
            try:
                refetch = requests.get(f"{API_BASE}/trips/{trip_id}", timeout=5, headers=headers)
                refetch.raise_for_status()
                trip = refetch.json()
            except Exception:
                trip = {"id": trip_id, "title": "Trip", "destination": "Unknown"}
            return render(request, "dashboard/trip_confirm_delete.html", {"trip": trip, "error": error})
        except Exception as e:
            try:
                refetch = requests.get(f"{API_BASE}/trips/{trip_id}", timeout=5, headers=headers)
                refetch.raise_for_status()
                trip = refetch.json()
            except Exception:
                trip = {"id": trip_id, "title": "Trip", "destination": "Unknown"}
            return render(request, "dashboard/trip_confirm_delete.html", {"trip": trip, "error": str(e)})

    try:
        resp = requests.get(f"{API_BASE}/trips/{trip_id}", timeout=5, headers=headers)
        resp.raise_for_status()
        trip = resp.json()
    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 404:
            return render(request, "dashboard/trip_not_found.html", status=404)
        return render(request, "dashboard/trip_list.html", {"trips": [], "error": f"Could not load trip: {e}"})
    except Exception as e:
        return render(request, "dashboard/trip_list.html", {"trips": [], "error": str(e)})

    return render(request, "dashboard/trip_confirm_delete.html", {"trip": trip})


@login_required_session
def trip_list_completed(request):
    """Show only completed trips."""
    headers = get_auth_headers(request)
    try:
        resp = requests.get(f"{API_BASE}/trips/status/completed", timeout=5, headers=headers)
        resp.raise_for_status()
        trips = resp.json()
    except Exception as e:
        trips = []
        error = str(e)
    else:
        error = None
    return render(request, "dashboard/trip_list.html", {
        "trips": trips, "error": error, "filter_label": "Completed Trips"
    })


@login_required_session
def trip_list_uncompleted(request):
    """Show only active/uncompleted trips."""
    headers = get_auth_headers(request)
    try:
        resp = requests.get(f"{API_BASE}/trips/status/uncompleted", timeout=5, headers=headers)
        resp.raise_for_status()
        trips = resp.json()
    except Exception as e:
        trips = []
        error = str(e)
    else:
        error = None
    return render(request, "dashboard/trip_list.html", {
        "trips": trips, "error": error, "filter_label": "Active Trips"
    })


@login_required_session
def trip_toggle_complete(request, trip_id):
    """Toggle trip completed/uncompleted via PATCH."""
    headers = get_auth_headers(request)
    if request.method == "POST":
        action = request.POST.get("action", "complete")
        endpoint = "complete" if action == "complete" else "uncomplete"
        try:
            resp = requests.patch(f"{API_BASE}/trips/{trip_id}/{endpoint}", timeout=5, headers=headers)
            resp.raise_for_status()
        except Exception:
            pass
    return redirect("trip-detail", trip_id=trip_id)

