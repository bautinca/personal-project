"""
SECCION PARA REGISTRAR LAS TABLAS ASI LAS RECONOCE EL ADMINISTRADOR DE DJANGO
"""

from django.contrib import admin

# Register your models here.
from .models import (
    Message,
    Room,
)  # Importamos las tablas para que las reconozca Django

admin.site.register(Room)  # Registramos la tabla Rooms
admin.site.register(Message)  # Registramos la tabla Messages
