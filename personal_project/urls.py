"""
ENDPOINTS (URLS) DEL PROYECTO EN GENERAL
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(
        "admin/", admin.site.urls
    ),  # Endpoint /admin/ que nos lleva a la vista de administracion de Django
    path(
        "", include("base.urls")
    ),  # Endpoint / que nos lleva a tener en cuenta los endpoints de la aplicacion 'base'
]
