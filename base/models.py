"""
ORM: OBJECT-RELATIONAL MAPPING (MAPEO DE OBJETO-RELACIONAL). PERMITE EL MAPEO DE OBJETOS A REGISTROS
DE TABLAS. NOS AHORRAMOS DE ESCRIBIR SQL DIRECTAMENTE. EL ORM HACE PUENTE ENTRE FILAS/COLUMNAS DE LAS TABLAS Y OBJETOS

INFRAESTRUCTURA ORM PURA, LE DICE A DJANGO COMO MAPEAR DE OBJETOS A LAS TABLAS
"""

# Importamos la tabla Users por defecto de Django
from django.contrib.auth.models import User
from django.db import models

# Tabla Rooms
class Room(models.Model):
    host = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )  # FK a la tabla Users, modo de eliminacion SET_NULL (si se elimina un usuario de la tabla Users, el campo host de la tabla Rooms se pone en NULL)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    topic = models.CharField(max_length=200, default="Programacion")
    # Timestamps
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']  # Ordenamos los registros de la tabla Rooms por fecha de actualizacion y creacion (de mas reciente a mas antiguo)

    def __str__(self):
        return self.name


# Tabla Mensajes
class Message(models.Model):
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE
    )  # FK a la tabla Rooms, modo de eliminacion CASCADA (si se elimina una fila de la tabla Rooms se eliminan todas las filas respectivas de la tabla Messages)
    body = models.TextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # FK a la tabla Users, modo de eliminacion CASCADA (si se elimina un usuario de la tabla Users se eliminan todos los mensajes respectivos de la tabla Messages)
    # Timestamps
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]
