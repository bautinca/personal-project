# Formulario para crear una nueva sala de chat
from django.forms import ModelForm

from .models import Room


class RoomForm(ModelForm):
  class Meta:
    model = Room
    fields = "__all__"