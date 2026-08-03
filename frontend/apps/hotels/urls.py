from django.urls import path
from . import views

urlpatterns = [
    path("search/", views.hotel_search, name="hotel-search"),
    path("history/", views.hotel_history, name="hotel-history"),
]
