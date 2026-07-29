                                                                                                            
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
                json={"email": email, "password": password},                                                        
                timeout=5,                                                                                          
            )                                                                                                       
            resp.raise_for_status()                                                                                 
            token = resp.json()["access_token"]                                                                     
            # Store the JWT in Django's session                                                                     
            request.session["access_token"] = token                                                                 
            request.session["user_email"] = email                                                                   
            return redirect("trip-list")  # redirect to dashboard after login                                       
        except requests.exceptions.HTTPError as e:                                                                  
            error = e.response.json().get("detail", "Login failed")                                                 
        except Exception as e:                                                                                      
            error = str(e)                                                                                          
        return render(request, "authentication/login.html", {"error": error})                                       
    return render(request, "authentication/login.html")     


def register(request):                                                                                              
    if request.method == "POST":                                                                                    
        payload = {                                                                                                 
            "username": request.POST.get("username"),                                                               
            "email": request.POST.get("email"),                                                                     
            "password": request.POST.get("password"),                                                               
        }                                                                                                           
        try:                                                                                                        
            resp = requests.post(f"{API_BASE}/auth/register", json=payload, timeout=5)                              
            resp.raise_for_status()                                                                                 
            return redirect("login")  # after register, go to login                                                 
        except requests.exceptions.HTTPError as e:                                                                  
            error = e.response.json().get("detail", "Registration failed")                                          
        except Exception as e:                                                                                      
            error = str(e)                                                                                          
        return render(request, "authentication/register.html", {"error": error})                                    
    return render(request, "authentication/register.html")


def logout(request):
    if request.method == "POST":
        request.session.flush()  # clear the JWT from session
        return redirect("login")
    return redirect("trip-list") # if someone visits /logout/ via GET, send them back
def hello(request):                                                                                                 
    from django.http import HttpResponse                                                                            
    return HttpResponse("Auth page")                                                                                
                                    