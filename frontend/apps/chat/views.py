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
def chat(request):
    """AI Chat page — sends a message to the backend and displays the reply."""
    headers = get_auth_headers(request)
    response_text = None
    error = None
    user_message = ""

    if request.method == "POST":
        user_message = request.POST.get("message", "").strip()
        if user_message:
            try:
                resp = requests.post(
                    f"{API_BASE}/chat/",
                    json={"message": user_message},
                    headers=headers,
                    timeout=30,
                )
                resp.raise_for_status()
                response_text = resp.json().get("response", "")
            except requests.exceptions.HTTPError as e:
                try:
                    error = e.response.json().get("detail", str(e))
                except Exception:
                    error = str(e)
            except Exception as e:
                error = str(e)
        else:
            error = "Please enter a message."

    return render(request, "chat/chat.html", {
        "user_message": user_message,
        "response_text": response_text,
        "error": error,
    })
