"""
EN LAS VIEWS REALIZAMOS LA LOGICA DE DISTINTOS ENDPOINTS ESPECIFICADOS
EN urls.py DE LA APLICACION 'BASE'
ES EL ADAPTADOR HTTP. TRADUCE REQUEST HTTP A LLAMADAS AL SERVICIO DE DOMINIO Y RESPUESTAS DEL DOMINIO EN RESPUESTAS
HTTP. NO TIENE LOGICA DE NEGOCIO POR TANTO ES OBVIO QUE VA POR FUERA DEL HEXAGONO
"""

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import (
    User,  # Importamos la tabla por defecto de Django User
)
from django.http import HttpResponse
from django.shortcuts import redirect, render

from base import models as base_models
from base.adapters.django_message_repository import DjangoMessageRepository
from base.adapters.django_room_repository import DjangoRoomRepository
from base.domain.entities.room import VALID_TOPICS
from base.domain.services.message_service import MessageService
from base.domain.services.room_service import (
    InvalidTopicError,
    RoomService,
    UnauthorizedError,
)
from base.forms import RoomForm
from base.models import Room


# Funciones helper
def _get_room_service() -> RoomService:
    return RoomService(repository=DjangoRoomRepository())

def _get_message_service() -> MessageService:
    return MessageService(repository=DjangoMessageRepository())

# ---------------------------------------

# Logica de logueo
def loginPage(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username OR password does not exist")

    return render(request, "./base/login_register.html", {"page": "login"})

# Logica de deslogueo
def logoutUser(request):
    logout(request)
    return redirect("home")

# Logica de registro
def registerPage(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error ocurred during registration")

    return render(request, "./base/login_register.html", {"form": form})

# Logica home page
def home(request):
    service = _get_room_service()
    rooms = service.get_all_rooms()
    return render(request, "./base/home.html", {"rooms": rooms})

# Logica pagina sala
def room(request, pk):
    service = _get_room_service()
    message_service = _get_message_service()

    try:
        room_entity = service.get_room(pk)
    except models.Room.DoesNotExist:
        return HttpResponse("Sala no encontrada", status=404)

    room_messages = message_service.get_room_messages(pk)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")
        message_service.send_message(
            room_id=pk,
            user_id=request.user.id,
            user_username=request.user.username,
            body=request.POST.get("body")
        )
        return redirect("room", pk=pk)

    return render(request, "./base/room.html", {
        "room": room_entity,
        "room_messages": room_messages,
    })

# Logica eliminar mensaje
@login_required(login_url="login")
def deleteMessage(request, room_id, message_id):
    if request.method != "POST":
        return HttpResponse("Metodo no permitido", status=405)

    service = _get_message_service()
    try:
        service.delete_message(
            message_id=message_id,
            requesting_user_id=request.user.id,
        )
    except UnauthorizedError:
        return HttpResponse("No autorizado", status=403)
    except base_models.Message.DoesNotExist:
        return HttpResponse("Mensaje no encontrado", status=404)

    return redirect("room", pk=room_id)

# Logica crear sala
@login_required(login_url="login")
def createRoom(request):

    if request.method == "POST":
        service = _get_room_service()
        try:
            service.create_room(
                name=request.POST.get("name"),
                host_id=request.user.id,
                topic=request.POST.get("topic"),
                description=request.POST.get("description", ""),
            )
            return redirect("home")
        except InvalidTopicError:
            messages.error(request, "Topic invalido")

    form = RoomForm()
    return render(request, "./base/room_form.html", {"form": form, "topics": VALID_TOPICS})

# Logica actualizar sala
@login_required(login_url="login")
def updateRoom(request, pk):
    service = _get_room_service()

    try:
        room_entity = service.get_room(pk)
    except Room.DoesNotExist:
        return HttpResponse("Sala no encontrada", status=404)

    if request.user.id != room_entity.host_id:
        return HttpResponse("No autorizado", status=403)

    if request.method == "POST":
        try:
            service.update_room(
                room_id=pk,
                requesting_user_id=request.user.id,
                name=request.POST.get("name"),
                topic=request.POST.get("topic"),
                description=request.POST.get("description", ""),
            )
            return redirect("home")
        except UnauthorizedError:
            return HttpResponse("No autorizado", status=403)
        except InvalidTopicError:
            messages.error(request, "Topic invalido")

    return render(request, "./base/room_form.html", {"room": room_entity, "topics": VALID_TOPICS})

# Logica eliminar sala
@login_required(login_url="login")
def deleteRoom(request, pk):
    service = _get_room_service()

    try:
        service.delete_room(room_id=pk, requesting_user_id=request.user.id)
    except UnauthorizedError:
        return HttpResponse("No autorizado", status=403)
    except Room.DoesNotExist:
        return HttpResponse("Sala no encontrada", status=404)

    return redirect("home")