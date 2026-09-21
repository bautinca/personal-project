"""
ENDPOINTS (URLS) DE LA APLICACION 'BASE'
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),  # Endpoint / de la aplicacion base
    path(
        "room/<str:pk>", views.room, name="room"
    ),  # Endpoint /room de la aplicacion base
    path("create-room/", views.createRoom, name="create-room"),  # Endpoint /create-room de la aplicacion base
    path("update-room/<str:pk>", views.updateRoom, name="update-room"),  # Endpoint /update-room de la aplicacion base
    path("delete-room/<str:pk>", views.deleteRoom, name="delete-room"),  # Endpoint /delete-room de la aplicacion base
    path("login/", views.loginPage, name="login"),  # Endpoint /login de la aplicacion base
    path("logout/", views.logoutUser, name="logout"),  # Endpoint /logout de la aplicacion base
    path("register/", views.registerPage, name="register"),  # Endpoint /register de la aplicacion base 
]
