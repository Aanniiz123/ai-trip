
from django.urls import path
from . import views

urlpatterns = [
    path("", views.trip_list, name="trip-list"),
    path("new/", views.trip_create, name="trip-create"),
]

