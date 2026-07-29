
from django.urls import path
from . import views

urlpatterns = [
    path("", views.trip_list, name="trip-list"),
    path("create/", views.trip_create, name="trip-create"),
    path("<int:trip_id>/", views.trip_detail, name="trip-detail"),
    path("<int:trip_id>/edit/", views.trip_edit, name="trip-edit"),
    path("<int:trip_id>/delete/", views.trip_delete, name="trip-delete"),
]