from django.shortcuts import render, redirect
import requests
from django.conf import settings

# Create your views here.

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
    """Fetch all the trips from the FastAPI backend and render them."""

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
    """Handle POST from the form to create a new trip."""
    headers = get_auth_headers(request) 
    if request.method == "POST":
        payload = {
            "title": request.POST.get("title"),
            "destination": request.POST.get("destination"),
            "start_date": request.POST.get("start_date"),
            "end_date": request.POST.get("end_date"),
        }
        try:
            resp = requests.post(f"{API_BASE}/trips/", json=payload, timeout=5, headers=headers)
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
    return render(request, "dashboard/trip_detail.html", {"trip": trip, "error": error})



@login_required_session
def trip_edit(request, trip_id):
    headers = get_auth_headers(request) 
    if request.method == "POST":
        payload = {
            "title": request.POST.get("title"),
            "destination": request.POST.get("destination"),
            "start_date": request.POST.get("start_date"),
            "end_date": request.POST.get("end_date"),
        }
        try:
            resp = requests.put(f"{API_BASE}/trips/{trip_id}", json=payload, timeout=5, headers=headers)
            resp.raise_for_status()
            return redirect("trip-detail", trip_id=trip_id)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 422:
                error = e.response.json().get("detail", str(e))
            else:
                error = str(e)
        except Exception as e:
            error = str(e)
        return render(request, "dashboard/trip_form.html", {
            "error": error, "trip": payload, "is_edit": True, "trip_id": trip_id
        })

    # GET — fetch existing trip to pre-fill form
    try:
        resp = requests.get(f"{API_BASE}/trips/{trip_id}", timeout=5)
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
        except Exception as e:
            return render(request, "dashboard/trip_detail.html", {
                "trip": {"id": trip_id}, "error": str(e)
            })
    # GET — show confirmation page
    try:
        resp = requests.get(f"{API_BASE}/trips/{trip_id}", timeout=5)
        resp.raise_for_status()
        trip = resp.json()
    except Exception as e:
        return render(request, "dashboard/trip_list.html", {"trips": [], "error": str(e)})
    return render(request, "dashboard/trip_confirm_delete.html", {"trip": trip})


def parse_api_error(resp, request):
    """Extract readable error from FastAPI response."""
    try:
        data = resp.json()
        if isinstance(data.get("detail"), list):
            return "; ".join(d["msg"] for d in data["detail"])
        return data.get("detail", resp.text)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:                                       
            request.session.flush()             
            return redirect("login")                                            
                                