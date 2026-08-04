from django.urls import path
from . import views

urlpatterns = [
    path("search/", views.place_search, name="place-search"),
    path("", views.place_list, name="place-list"),
    path("<int:place_id>/delete/", views.place_delete, name="place-delete"),
]
