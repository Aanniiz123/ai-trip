from django.shortcuts import render, redirect
from django.conf import settings
import requests

API_BASE = getattr(settings, "API_BASE_URL", "http://127.0.0.1:8000")


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            resp = requests.post(
                f"{API_BASE}/auth/login",
                json={
                    "email": email,
                    "password": password,
                },
                timeout=5,
            )

            resp.raise_for_status()

            token = resp.json()["access_token"]

            # Store JWT in session
            request.session["access_token"] = token
            request.session["user_email"] = email

            return redirect("trip-list")

        except requests.exceptions.HTTPError as e:
            error = e.response.json().get("detail", "Login failed")
        except Exception as e:
            error = str(e)

        return render(
            request,
            "authentication/login.html",
            {"error": error},
        )

    return render(request, "authentication/login.html")


def register(request):
    if request.method == "POST":
        payload = {
            "username": request.POST.get("username"),
            "email": request.POST.get("email"),
            "password": request.POST.get("password"),
        }

        try:
            resp = requests.post(
                f"{API_BASE}/auth/register",
                json=payload,
                timeout=5,
            )

            resp.raise_for_status()

            # Register succeeded — now log in to get a token
            data = resp.json()
            login_resp = requests.post(
                f"{API_BASE}/auth/login",
                json={
                    "email": payload["email"],
                    "password": payload["password"],
                },
                timeout=5,
            )
            login_resp.raise_for_status()
            token = login_resp.json()["access_token"]
            request.session["access_token"] = token
            request.session["user_email"] = payload["email"]

            return redirect("user_info")

        except requests.exceptions.HTTPError as e:
            error = e.response.json().get("detail", "Registration failed")
        except Exception as e:
            error = str(e)

        return render(
            request,
            "authentication/register.html",
            {"error": error},
        )

    return render(request, "authentication/register.html")


def user_info(request):
    # Get JWT from session
    token = request.session.get("access_token")

    # User must be logged in
    if not token:
        return redirect("login")

    if request.method == "POST":
        payload = {
            "phone": request.POST.get("phone"),
            "education": request.POST.get("education"),
            "job_title": request.POST.get("job_title"),
            "current_location": request.POST.get("current_location"),
            "nationality": request.POST.get("nationality"),
            "date_of_birth": request.POST.get("date_of_birth"),
        }

        headers = {
            "Authorization": f"Bearer {token}"
        }

        try:
            resp = requests.put(
                f"{API_BASE}/users/me/profile",
                json=payload,
                headers=headers,
                timeout=5,
            )

            resp.raise_for_status()

            return redirect("trip-list")

        except requests.exceptions.HTTPError as e:
            try:
                error = e.response.json().get("detail", "Failed to save profile")
            except Exception:
                error = "Failed to save profile"

        except requests.exceptions.RequestException as e:
            error = f"Connection error: {e}"

        except Exception as e:
            error = str(e)

        return render(
            request,
            "authentication/user_info.html",
            {"error": error},
        )

    return render(request, "authentication/user_info.html")


def profile(request):
    """View and edit user profile details."""
    token = request.session.get("access_token")
    if not token:
        return redirect("login")

    headers = {"Authorization": f"Bearer {token}"}
    success = None
    error = None

    # Fetch current user + profile data
    try:
        user_resp = requests.get(f"{API_BASE}/users/me", headers=headers, timeout=5)
        user_resp.raise_for_status()
        user_data = user_resp.json()
    except Exception as e:
        user_data = {}
        error = str(e)

    try:
        profile_resp = requests.get(f"{API_BASE}/users/me/profile", headers=headers, timeout=5)
        profile_resp.raise_for_status()
        profile_data = profile_resp.json()
    except Exception:
        profile_data = {}

    if request.method == "POST":
        payload = {
            "phone": request.POST.get("phone"),
            "education": request.POST.get("education"),
            "job_title": request.POST.get("job_title"),
            "current_location": request.POST.get("current_location"),
            "nationality": request.POST.get("nationality"),
            "date_of_birth": request.POST.get("date_of_birth") or None,
        }
        try:
            resp = requests.put(
                f"{API_BASE}/users/me/profile",
                json=payload,
                headers=headers,
                timeout=5,
            )
            resp.raise_for_status()
            profile_data = resp.json()
            success = "Profile updated successfully!"
        except requests.exceptions.HTTPError as e:
            try:
                error = e.response.json().get("detail", "Failed to update profile")
            except Exception:
                error = "Failed to update profile"
        except Exception as e:
            error = str(e)

    return render(request, "authentication/profile.html", {
        "user": user_data,
        "profile": profile_data,
        "success": success,
        "error": error,
    })


def change_password(request):
    """Change the logged-in user's password."""
    token = request.session.get("access_token")
    if not token:
        return redirect("login")

    headers = {"Authorization": f"Bearer {token}"}
    success = None
    error = None

    if request.method == "POST":
        new_password = request.POST.get("new_password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not new_password:
            error = "New password cannot be empty."
        elif new_password != confirm_password:
            error = "Passwords do not match."
        else:
            try:
                resp = requests.put(
                    f"{API_BASE}/users/me",
                    json={"password": new_password},
                    headers=headers,
                    timeout=5,
                )
                resp.raise_for_status()
                success = "Password changed successfully!"
            except requests.exceptions.HTTPError as e:
                try:
                    error = e.response.json().get("detail", "Failed to change password")
                except Exception:
                    error = "Failed to change password"
            except Exception as e:
                error = str(e)

    return render(request, "authentication/change_password.html", {
        "success": success,
        "error": error,
    })


def logout(request):
    if request.method == "POST":
        request.session.flush()
        return redirect("login")

    return redirect("trip-list")