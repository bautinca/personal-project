from behave import given, then, when
from bs4 import BeautifulSoup
from django.test import Client


@when('el usuario entra a la sala "{name}" y envia el mensaje "{body}"')
def step_enter_room_and_send_message(context, name, body):
  response = context.client.get("/")
  assert response.status_code == 200

  soup = BeautifulSoup(response.content, 'html.parser')
  room_link = soup.find('a', string=name, href=True)
  assert room_link is not None, f"No se encontró el enlace de la sala '{name}'"

  room_url = room_link['href']
  response = context.client.get(room_url)
  assert response.status_code == 200, f"Error al acceder a la sala: got {response.status_code}"

  response = context.client.post(room_url, {
      "body": body,
  })
  assert response.status_code == 302, f"Error al enviar mensaje: got {response.status_code}"

  context.room_url = room_url  # Guardamos la URL de la sala en el contexto para usarla en el siguiente paso

@then('el mensaje "{body}" aparece en la sala "{name}"')
def step_message_visible(context, body, name):
  response = context.client.get(context.room_url)
  assert response.status_code == 200
  assert body.encode() in response.content, f"El mensaje '{body}' no aparece en la sala '{name}'"

@when('el usuario no registrado entra a la sala "{name}"')
def step_non_registered_user_enters_room(context, name):
  response = context.client.get("/")
  assert response.status_code == 200

  soup = BeautifulSoup(response.content, 'html.parser')
  room_link = soup.find('a', string=name, href=True)
  assert room_link is not None, f"No se encontró el enlace de la sala '{name}'"

  room_url = room_link['href']
  response = context.client.get(room_url)
  assert response.status_code == 200, f"Error al acceder a la sala: got {response.status_code}"

  context.response = response  # Guardamos la respuesta en el contexto para usarla en el siguiente paso

@then('no ve el formulario para enviar mensajes')
def step_non_message_form_visible(context):
  soup = BeautifulSoup(context.response.content, 'html.parser')
  form = soup.find('form')
  assert form is None, "El usuario no registrado deberia no ver el formulario para enviar mensajes en la sala"

@then('ve el boton "{button_text}" para el mensaje "{body}"')
def step_delete_button_visible(context, button_text, body):
  response = context.client.get(context.room_url)
  soup = BeautifulSoup(response.content, 'html.parser')
  message = soup.find(string=body)
  assert message is not None, f"No se encontró el mensaje '{body}'"
  message_container = message.find_parent('div')
  button = message_container.find('button', string=button_text)
  assert button is not None, f"No se encontró el botón '{button_text}' para el mensaje '{body}'"

@when('elimina el mensaje "{body}"')
def step_delete_message(context, body):
  response = context.client.get(context.room_url)
  soup = BeautifulSoup(response.content, 'html.parser')
  message = soup.find(string=body)
  assert message is not None, f"No se encontró el mensaje '{body}'"
  message_container = message.find_parent('div')
  delete_form = message_container.find('form')
  assert delete_form is not None, f"No se encontró el formulario para eliminar el mensaje '{body}'"

  context.response = context.client.post(delete_form['action'])
  assert context.response.status_code == 302

@then('el mensaje "{body}" ya no aparece en la sala "{name}"')
def step_message_not_visible(context, body, name):
  response = context.client.get(context.room_url)
  assert response.status_code == 200
  assert body.encode() not in response.content, f"El mensaje '{body}' todavía aparece en la sala '{name}'"

@given('que existe un mensaje "{body}" creado por "{username}"')
def step_existing_message(context, body, username):
  response = context.client.get("/")
  assert response.status_code == 200
  soup = BeautifulSoup(response.content, 'html.parser')
  room_link = soup.find('a', string="Sala Python", href=True)
  assert room_link is not None, "No se encontró el enlace de la sala 'Sala Python'"
  context.room_url = room_link['href']
  response = context.client.post(context.room_url, {"body": body})
  assert response.status_code == 302

@given('que el usuario "{username}" se registra e inicia sesion con password "{password}"')
def step_register_and_login_another_user(context, username, password):
  context.client = Client()
  response = context.client.post("/register/", {
      "username": username,
      "password1": password,
      "password2": password,
  })
  assert response.status_code == 302

@when('el usuario "{username}" entra a la sala "{name}"')
def step_another_user_enters_room(context, username, name):
  response = context.client.get("/")
  assert response.status_code == 200
  soup = BeautifulSoup(response.content, 'html.parser')
  room_link = soup.find('a', string=name, href=True)
  assert room_link is not None, f"No se encontró el enlace de la sala '{name}'"

  context.room_url = room_link['href']
  context.response = context.client.get(context.room_url)
  assert context.response.status_code == 200

@then('no ve el boton "{button_text}" para el mensaje "{body}"')
def step_delete_button_not_visible(context, button_text, body):
  soup = BeautifulSoup(context.response.content, 'html.parser')
  message = soup.find(string=body)
  assert message is not None, f"No se encontró el mensaje '{body}'"
  message_container = message.find_parent('div')
  button = message_container.find('button', string=button_text)
  assert button is None, f"El botón '{button_text}' no debería aparecer para el mensaje '{body}'"