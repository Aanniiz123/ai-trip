
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name = 'register'),
    path('user_info/', views.user_info, name = 'user_info'),
    path('login/', views.login, name = 'login'),
    path("logout/", views.logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("change-password/", views.change_password, name="change-password"),
]