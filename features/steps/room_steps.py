from behave import given, when, then
from django.test import Client
# Usamos la libreria BeautifulSoup para parsear el HTML y obtener el ID de la sala a editar
from bs4 import BeautifulSoup

@given('que el usuario completa el formulario de registro con username "{username}" y password "{password}"')
def step_register_user(context, username, password):
    context.client = Client()
    response = context.client.post("/register/", { # El cliente va al endpoint de registro y envía los datos del usuario para registrarse en un request HTTP POST
        "username": username,
        "password1": password,
        "password2": password,
    })

    assert response.status_code == 302, f"Error al registrar usuario: got {response.status_code}"

@given('que el usuario completa el formulario de login con username "{username}" y password "{password}"')
def step_login_user(context, username, password):
    response = context.client.post("/login/", { # El cliente va al endpoint de login y envía los datos del usuario para iniciar sesión en un request HTTP POST
        "username": username,
        "password": password,
    })
    assert response.status_code == 302, f"Error al iniciar sesión: got {response.status_code}"

@when('el usuario completa el formulario de crear sala con nombre "{name}" y topic "{topic}" y descripcion "{description}"')
def step_create_room(context, name, topic, description):
    response = context.client.post("/create-room/", {
        "name": name,
        "topic": topic,
        "description": description,
    })
    assert response.status_code == 302, f"Error al crear sala: got {response.status_code}"

@then('el usuario es redirigido al home y ve la sala "{name}" en la lista')
def step_room_visible_in_home(context, name):
    response = context.client.get("/")
    assert response.status_code == 200
    assert name.encode() in response.content, f"Sala '{name}' no encontrada en la lista de salas"

@given('que el usuario no esta autenticado')
def step_user_not_authenticated(context):
    context.client = Client()  # Se crea un cliente de prueba sin autenticación

@when('el usuario intenta acceder a la pagina de crear sala')
def step_access_create_room(context):
    context.response = context.client.get("/create-room/")  # Se intenta acceder a la página de crear sala

@then('es redirigido a la pagina de login')
def step_redirected_to_login(context):
    assert context.response.status_code == 302
    assert "/login" in context.response["Location"], "No se redirigió a la página de login"

@when('el host edita la sala "{old_name}" cambiando el nombre a "{new_name}" y topic "{new_topic}" y descripcion "{new_description}"')
def step_edit_room(context, old_name, new_name, new_topic, new_description):
    response = context.client.get("/")  # Vamos al main page donde esta la lista de salas creadas
    assert response.status_code == 200

    # Parseamos el HTML para buscar el link de edicion de sala 'Edit'
    soup = BeautifulSoup(response.content, 'html.parser') # Parseamos el contenido HTML de la respuesta usando BeautifulSoup

    # Buscamos el enlace de edición de la sala
    # Buscamos el enlace con la etiqueta <a> que tenga el texto 'Edit' y un atributo href (el link de edicion de la sala)
    edit_link = soup.find('a', string='Edit', href=True)
    assert edit_link is not None, f"No se encontró el enlace de edición para la sala '{old_name}'"

    # Entramos al formulario de edicion de la sala usando el link de edicion
    edit_url = edit_link['href']
    response = context.client.get(edit_url)
    assert response.status_code == 200, f"Error al acceder al formulario de edición: {response.status_code}"

    # Enviamos el formulario de edicion con los nuevos datos
    response = context.client.post(edit_url, {
        "name": new_name,
        "topic": new_topic,
        "description": new_description,
    })
    assert response.status_code == 302, f"Error al editar sala: got {response.status_code}"

@given('que el usuario crea una sala con nombre "{name}" y topic "{topic}" y descripcion "{description}"')
def step_given_create_room(context, name, topic, description):
    response = context.client.post("/create-room/", {
        "name": name,
        "topic": topic,
        "description": description,
    })
    assert response.status_code == 302, f"Error al crear sala: got {response.status_code}"

@when('el usuario no host ve la lista de salas')
def step_non_host_views_home(context):
    context.response = context.client.get("/")
    assert context.response.status_code == 200, f"Error al acceder a la lista de salas: got {context.response.status_code}"

@then('no ve la opcion de editar la sala "{name}"')
def step_no_edit_option_visible(context, name):
    soup = BeautifulSoup(context.response.content, 'html.parser')
    edit_links = soup.find_all('a', string="Edit")
    assert len(edit_links) == 0, f"El usuario no host debería no ver la opción de editar la sala '{name}'"

@when('el host le da click al boton de eliminar de la sala "{name}"')
def step_delete_room_as_host(context, name):
    response = context.client.get("/")
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, 'html.parser')
    delete_link = soup.find('a', string="Delete", href=True)
    assert delete_link is not None, f"No se encontró el enlace de eliminación para la sala '{name}'"

    delete_url = delete_link['href']
    response = context.client.post(delete_url)
    assert response.status_code == 302, f"Error al eliminar sala: got {response.status_code}"

@then('la sala "{name}" no aparece en la lista de salas')
def step_room_not_visible(context, name):
    response = context.client.get("/")
    assert response.status_code == 200
    assert name.encode() not in response.content, f"Sala '{name}' aún aparece en la lista de salas"

@then('no ve la opcion de eliminar la sala "{name}"')
def step_no_delete_option_visible(context, name):
    soup = BeautifulSoup(context.response.content, 'html.parser')
    delete_links = soup.find_all('a', string="Delete")
    assert len(delete_links) == 0, f"El usuario no host debería no ver la opción de eliminar la sala '{name}'"